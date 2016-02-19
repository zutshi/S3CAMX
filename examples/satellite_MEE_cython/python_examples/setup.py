# Reference: http://stackoverflow.com/questions/16993927/using-cython-to-link-python-to-a-shared-library

# setup.py file
import numpy
import os
import shutil

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

# clean previous build
#for root, dirs, files in os.walk(".", topdown=False):
#    for name in files:
#        if (name.startswith("artificial_pancreas") and not(name.endswith(".pyx") or name.endswith(".pxd"))):
#            os.remove(os.path.join(root, name))
#    for name in dirs:
#        if (name == "build"):
#            shutil.rmtree(name)

# build "myext.so" python extension to be added to "PYTHONPATH" afterwards...
setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("sat",
                  include_dirs=[numpy.get_include()],
                  sources=["sat.pyx"],
                  libraries=['satellite_MEE'],          # refers to "libexternlib.so"
                  language="c++",                   # remove this if C and not C++
                  extra_compile_args=["-fopenmp", "-O3"],
                  extra_link_args=[]
             )
        ]
)
