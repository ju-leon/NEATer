from setuptools import setup

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from pybind11 import get_cmake_dir

import sys

__version__ = "0.0.1"

# The main interface is through Pybind11Extension.
# * You can add cxx_std=11/14/17, and then build_ext can be removed.
# * You can set include_pybind11=false to add the include directory yourself,
#   say from a submodule.
#
# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension("_neat",
                      [
                          "neater/ext/ext.cpp",
                          "neater/ext/network/Network.cpp",
                          "neater/ext/network/graph/src/Node.cpp",
                          "neater/ext/network/graph/src/Edge.cpp",
                          "neater/ext/network/graph/src/InputNode.cpp",
                          "neater/ext/Genome.cpp",
                          "neater/ext/genes/EdgeGene.cpp",
                          "neater/ext/genes/NodeGene.cpp",
                      ],
                      include_dirs=[
                          # Path to pybind11 headers
                          "neater/ext/network",
                          "neater/ext/network/include",
                          "neater/ext"
                          "neater/ext/genes"
                      ],
                      # Example: passing in the version to the compiled code
                      define_macros=[('VERSION_INFO', __version__)],
                      ),
]

setup(
    name="neat",
    version=__version__,
    author="Leon Jungemeyer",
    author_email="sylvain.corlay@gmail.com",
    url="https://github.com/pybind/python_example",
    description="A test project using pybind11",
    long_description="",
    ext_modules=ext_modules,
    # extras_require={"test": "pytest"},
    # Currently, build_ext only provides an optional "highest supported C++
    # level" feature, but in the future it may provide more features.
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)
