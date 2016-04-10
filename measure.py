#!/usr/bin/env python3

# A script to measure the effect of different optimization flags.

import os, sys, subprocess, shutil, time

# If your system static linker does not support lto you may
# need to run like this:
#
# AR=gcc-ar CC=gcc ./measure.py

# This script is tuned to my development machine, where
# Meson binaries are not in the path. If you wish to run this
# yourself, update these.

if os.path.exists('/home/jpakkane/meson/meson.py'):
    meson = '/home/jpakkane/meson/meson.py'
    mesonconf = '/home/jpakkane/meson/mesonconf.py'
else:
    meson = '/home/jpakkane/workspace/meson/meson.py'
    mesonconf = '/home/jpakkane/workspace/meson/mesonconf.py'

# In our test: swift-2.2-SNAPSHOT-2015-12-01-b-ubuntu15.10.tar
test_data = os.path.join(os.getcwd(), 'testdata')
# In our test: gzip_1.6.orig.tar
train_data = os.path.join(os.getcwd(), 'traindata')

def setup(extra_args = []):
    try:
        shutil.rmtree('build')
    except:
        pass
    os.mkdir('build')
    subprocess.check_call([meson, 'build'] + extra_args,
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

def compile(pgo):
    subprocess.check_call(['ninja', '-C', 'build', '-v'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    if pgo:
        subprocess.check_call('zpipe < {} > /dev/null'.format(train_data), shell=True, cwd='build')
        subprocess.check_call([mesonconf, 'build', '-Db_pgo=use'])
        subprocess.check_call(['ninja', '-C', 'build', '-v'],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )

def measure():
    times = []
    for _ in range(5):
        start = time.time()
        subprocess.check_call('build/zpipe < {} > /dev/null'.format(test_data), shell=True)
        end = time.time()
        times.append(end - start)
    return min(times)

def measure_buildtypes(setup_args, pgo=False):
    setup(setup_args + ['--buildtype=debugoptimized'])
    compile(pgo)
    dopt_t = measure()
    print('Debugopt took:', dopt_t)
    setup(setup_args + ['--buildtype=release'])
    compile(pgo)
    rel_t = measure()
    print('Release took:', rel_t)

if __name__ == '__main__':
    if not os.path.exists('meson.build'):
        print('Run this script at the top of the source tree.')
        sys.exit(1)
    print('Basic optimizations, shared library')
    measure_buildtypes([])
    print('\nBasic optimizations, static library')
    measure_buildtypes(['--default-library=static'])
    print('\nUsing lto, static')
    measure_buildtypes(['--default-library=static', '-Db_lto=true'])
    print('\nUsing pgo, static')
    measure_buildtypes(['--default-library=static', '-Db_pgo=generate'], True)
    print('\nUsing lto and pgo, static')
    measure_buildtypes(['--default-library=static', '-Db_lto=true', '-Db_pgo=generate'], True)
