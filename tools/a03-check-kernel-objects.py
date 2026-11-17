#!/usr/bin/env python3
"""Replay CI per-file Clang commands on an extracted XNU buildtree.

Preserves preprocessor definitions, include order, warning policy and generated
headers. Remaps runner paths; uses local Clang with the same Apple arm64 target.
The buildtree must already contain the candidate patched source. This checks C
compilation, not Xcode-specific behavior, kernel linkage or hardware operation.
C++ uses clang++; unsupported Apple allocation builtins are reported as errors,
not silently replaced. This tool never adds host-only builtin substitutions.
"""
import argparse
import json
from pathlib import Path
import re
import shlex
import subprocess
import sys


def command_for(log, source, tree, compiler, output):
    candidates=[]
    for line in log.splitlines():
        if '/xnu/'+source not in line:
            continue
        if ' -c ' not in line or not re.search(r'/clang(?:\+\+)?(?:\s|$)',line):
            continue
        start=line.find('ccache ')
        start=start+7 if start>=0 else line.find('/Applications/')
        if start<0:
            continue
        args=shlex.split(line[start:])
        matches=[arg for arg in args if arg.endswith('/xnu/'+source)]
        if len(matches)==1:
            candidates.append((args,matches[0].removesuffix('/xnu/'+source)))
    if not candidates:
        raise ValueError('no CI compile command for '+source)
    args,prefix=candidates[-1]
    result=[compiler,'-target','arm64-apple-macos15','-Wno-unknown-warning-option']
    i=1
    while i<len(args):
        arg=args[i]
        if arg=='-arch':
            if args[i+1]!='arm64':raise ValueError('unexpected target architecture')
            i+=2;continue
        if arg in ('-o','-MF','-MT','-dependency-file'):
            i+=2;continue
        if arg.startswith('-I/Applications/'):
            # CI archives these SDK platform headers alongside the build tree.
            result.append('-I'+str(tree/'sdk-kernel-platform/platform'))
        else:
            result.append(arg.replace(prefix,str(tree)))
        i+=1
    result+=['-o',str(output)]
    # BSD and Mach compilation use different visibility and include paths.
    # Never add MACH_KERNEL_PRIVATE or suppress language diagnostics here.
    component=source.split('/',1)[0]
    if component not in ('osfmk','bsd','iokit','libkern','pexpert'):
        raise ValueError('unsupported source component '+component)
    cwd=tree/'build/xnu.obj/DEVELOPMENT_ARM64_SWEET'/component/'DEVELOPMENT'
    return result,cwd


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('tree',type=Path)
    p.add_argument('log',type=Path)
    p.add_argument('sources',nargs='+')
    p.add_argument('--clang',default='clang')
    p.add_argument('--clangxx',default='clang++',help='C++ driver; Apple allocation builtins still require Xcode')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();tree=a.tree.resolve();a.output.mkdir(parents=True,exist_ok=True)
    log=a.log.read_text(errors='replace');failed=False
    for source in a.sources:
        output=(a.output/(source.replace('/','_')+'.o')).resolve()
        compiler=a.clangxx if source.endswith(('.cpp','.cc','.cxx')) else a.clang
        cmd,cwd=command_for(log,source,tree,compiler,output)
        (output.with_suffix('.command.json')).write_text(json.dumps({'cwd':str(cwd),'argv':cmd},indent=2)+'\n')
        r=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        output.with_suffix('.log').write_text(r.stdout)
        errors=[line for line in r.stdout.splitlines() if 'error:' in line]
        print(('FAIL ' if r.returncode else 'PASS ')+source)
        for line in errors[:12]:print(line)
        failed|=r.returncode!=0
    return int(failed)


if __name__=='__main__':
    sys.exit(main())
