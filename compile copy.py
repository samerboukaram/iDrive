#Reference:
#https://medium.com/@xpl/protecting-python-sources-using-cython-dcd940bb188e

#Run this file with the following arguments:
#python3 compile.py build_ext --inplace

import iOS

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

AllSrcipts = iOS.GetAllPythonScripts()
print(AllSrcipts)

Ext_Modules = []

for Script in AllSrcipts:
    print(Script[:-3])
    Ext_Modules.append(Extension(Script[:-3],[Script]))

# ext_modules = [
#     Extension("iDrive",  ["iDrive.py"]),
#     # Extension("mymodule2",  ["mymodule2.py"]),
    
# #   ... all your modules that need be compiled ...

# ]


setup(
    name = 'My Program Name',
    cmdclass = {'build_ext': build_ext},
    ext_modules = Ext_Modules
)