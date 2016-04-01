project('zlib speed test', 'c')

zproj = subproject('zlib')
z_lib = zproj.get_variable('zlib')
z_inc = zproj.get_variable('incdir')

executable('zpipe', 'zpipe.c',
           include_directories : z_inc,
           link_with : z_lib)

