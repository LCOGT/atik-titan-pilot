from distutils.core import setup, Extension

import os

base_dir = os.path.dirname(os.path.realpath(__file__))

module_artemishsc = Extension("_artemishsc", ["artemishsc.i", "ArtemisHscAPI.cpp"],
                              define_macros=[('DEBUG', True)],
                              include_dirs=[r"c:\Python27\Lib\site-packages\numpy\core\include"],
                              library_dirs=[
                                  r"c:\Python27\libs",
                                  r"{base_dir!s}\shared".format(**locals()),
                                  r"c:\Program Files (x86)\mingw\mingw32\i686-w64-mingw32\lib"],
                              libraries=["ArtemisHSC", "oleaut32"])

setup(name="Atik Titan API", version="1.0", ext_modules=[module_artemishsc], requires=['pyfits', 'numpy'])
