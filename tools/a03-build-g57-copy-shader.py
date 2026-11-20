#!/usr/bin/env python3
"""Reproduce private G57 copy binary using an already configured Mesa24.3 build.

Requires native Mesa24.3.0 configured with tools=panfrost, compile_commands.json,
and the bifrost_compiler executable target. No phone access or kernel staging.
"""
import argparse,hashlib,json,re,shlex,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('mesa_build',type=Path);p.add_argument('output',type=Path)
modes=p.add_mutually_exclusive_group()
modes.add_argument('--blit',action='store_true',help='reproduce bounded four-pixel 16x4 strided blit shader')
modes.add_argument('--fullscreen',action='store_true',help='reproduce exact 720x1600 fifteen-by-four fullscreen shader')
a=p.parse_args()
build=a.mesa_build.resolve();out=a.output.resolve()
if out.exists():p.error('output directory exists')
info=json.loads(subprocess.check_output(['meson','introspect',str(build),'--projectinfo']))
if info['version']!='24.3.0':p.error('requires pinned Mesa24.3.0')
subprocess.run(['ninja','-C',str(build),'-j8','src/panfrost/bifrost_compiler'],check=True)
commands=json.loads((build/'compile_commands.json').read_text())
e=next(c for c in commands if c['file'].endswith('/compiler/cmdline.c'))
args=e.get('arguments') or shlex.split(e['command'])
# Preserve authoritative compiler, defines and include order from Mesa's own target.
filtered=[];skip=False
for item in args:
 if skip:skip=False;continue
 if item in ('-o','-MF','-MQ','-MT'):skip=True;continue
 if item in ('-MD','-MMD','-c') or item.endswith('/compiler/cmdline.c'):continue
 filtered.append(item)
source=(Path(e['directory'])/e['file']).resolve().parents[1]
out.mkdir(parents=True)
obj=out/'copygen.o';exe=out/'copygen';binary=out/'g57-copy.bin'
filtered+=['-I'+str(source/'compiler/valhall'),'-I'+str(build/'src/panfrost/compiler/valhall'),'-c',str(ROOT/'tools'/('a03-g57-fullscreen-shader.c' if a.fullscreen else 'a03-g57-blit-shader.c' if a.blit else 'a03-g57-copy-shader.c')),'-o',str(obj)]
subprocess.run(filtered,cwd=build,check=True)
lines=subprocess.check_output(['ninja','-C',str(build),'-t','commands','src/panfrost/bifrost_compiler'],text=True).splitlines()
link=shlex.split(lines[-1]);i=link.index('-o');link[i+1]=str(exe)
assert any(x.endswith('compiler_cmdline.c.o') for x in link)
link=[str(obj) if x.endswith('compiler_cmdline.c.o') else x for x in link]
subprocess.run(link,cwd=build,check=True)
with (out/'g57-copy.disasm').open('w') as dis,(out/'g57-copy.info').open('w') as log:
 subprocess.run([str(exe),str(binary)],stdout=dis,stderr=log,check=True)
header=(ROOT/'tools'/('a03-gpu-blit-layout.h' if a.blit or a.fullscreen else 'a03-gpu-copy-layout.h')).read_text()
expected=re.search(('Exact full-screen shader SHA256 ' if a.fullscreen else 'SHA256 ' if a.blit else 'Binary SHA256: ')+r'([0-9a-f]{64})',header)[1]
actual=hashlib.sha256(binary.read_bytes()).hexdigest()
if actual!=expected:raise SystemExit('generated binary differs: '+actual+' expected '+expected)
print('PASS reproduced pinned G57 copy shader SHA256 '+actual)
