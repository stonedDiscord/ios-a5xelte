#!/usr/bin/env python3
"""Check exact CI command remapping for C and C++ component compiles."""
import importlib.util
from pathlib import Path
sp=importlib.util.spec_from_file_location('check',Path(__file__).with_name('a03-check-kernel-objects.py'))
m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
root=Path('/local/tree');output=Path('/tmp/result.o')
for component,source,driver in [('bsd','bsd/kern/sweet_amfi.c','clang'),
                               ('osfmk','osfmk/kern/task.c','clang'),
                               ('iokit','iokit/Kernel/arm/SweetKeyStore.cpp','clang++'),
                               ('libkern','libkern/c++/OSObject.cpp','clang++')]:
    log=f'''step ccache /Applications/Xcode.app/bin/{driver} -o old.o -c -arch arm64 -std=gnu++17 -DKEEP_ME -mgeneral-regs-only -I/runner/tree/xnu/osfmk -I/Applications/SDK/platform -MD -MF old.d -MP /runner/tree/xnu/{source}'''
    args,cwd=m.command_for(log,source,root,driver,output)
    assert args[0]==driver and args[-2:]==['-o',str(output)]
    assert cwd==root/'build/xnu.obj/DEVELOPMENT_ARM64_SWEET'/component/'DEVELOPMENT'
    assert '-DKEEP_ME' in args and '-mgeneral-regs-only' in args
    assert '-I/local/tree/xnu/osfmk' in args and '-I/local/tree/sdk-kernel-platform/platform' in args
    assert '/local/tree/xnu/'+source in args
    assert not any(x in args for x in ('-arch','old.o','old.d','-MF'))
try:m.command_for('', 'bsd/kern/sweet_amfi.c',root,'clang',output)
except ValueError:pass
else:raise AssertionError('missing command accepted')
print('PASS CI command replay: C/C++ driver detection, BSD/Mach/IOKit/libkern cwd, exact flags/includes, output/dependency remapping, missing source rejection')
