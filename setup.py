import distutils
from distutils.core import setup, Extension

import os

base_dir = os.path.dirname(os.path.realpath(__file__))

module_artemishsc = Extension("_artemishsc", ["artemishsc.i", "ArtemisHscAPI.cpp"],
                                include_dirs = [],
                                library_dirs = [r"c:\Python27\libs", r"{base_dir!s}\shared".format(**locals())],
                                libraries = ["ArtemisHSC"])

setup(name = "Atik Titan API", version="1.0", ext_modules = [module_artemishsc])
