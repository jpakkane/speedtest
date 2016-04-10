# Compiler optimisation test

This repository contains a benchmark app that compiles zlib with a
bunch of different optimization settings.

The results are examined in [this blog
post](http://nibblestew.blogspot.com/2016/04/testing-performance-of-build.html).

To run the tests yourself you just need the [Meson build
system](http://mesonbuild.com). You don't need to get zlib source
yourself, it will automatically download it from the
[wrapdb](https://github.com/mesonbuild/meson/wiki/Wrap%20dependency%20system%20manual).

The steps are simple:

 - clone this repo
 - edit `measure.py` to point to your Meson binaries
 - read the comments to see if you need to set some environment variables
 - run 'measure.py`
