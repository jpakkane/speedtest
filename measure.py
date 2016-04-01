#!/usr/bin/env python3

# A script to measure the effect of different optimization flags.

import os, sys, subprocess, shutil, time

# This script is tuned to my development machine, where
# Meson binaries are not in the path. If you wish to run this
# yourself, update these.

meson = '/home/jpakkane/workspace/meson/meson.py'
mesonconf = '/home/jpakkane/workspace/meson/mesonconf.py'

# In our test: swift-2.2-SNAPSHOT-2015-12-01-b-ubuntu15.10.tar
test_data = os.path.join(os.getcwd(), 'testdata')
# In our test: gzip_1.6.orig.tar
train_data = os.path.join(os.getcwd(), 'traindata')

def setup():
    try:
        shutil.rmtree('build')
    except:
        pass
    os.mkdir('build')
    subprocess.check_call([meson, 'build'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

def compile():
    subprocess.check_call(['ninja', '-C', 'build'],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )

def measure():
    times = []
    for _ in range(1):
        start = time.time()
        subprocess.check_call('build/zpipe < {} > /dev/null'.format(test_data), shell=True)
        end = time.time()
        times.append(end - start)
    return min(times)

if __name__ == '__main__':
    if not os.path.exists('meson.build'):
        print('Run this script at the top of the source tree.')
        sys.exit(1)
    setup()
    compile()
    debug_t = 1#measure()
    print('Debug took:', debug_t)
    time.sleep(1)
    subprocess.check_call([mesonconf, 'build', '-Dbuildtype=debugoptimized'])
    compile()
    dopt_t = measure()
    print('Debugopt took:', dopt_t)
    subprocess.check_call([mesonconf, 'build', '-Dbuildtype=release'])
    compile()
    rel_t = measure()
    print('Release took:', dopt_t)
