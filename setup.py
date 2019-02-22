#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

<<<<<<< HEAD
# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs

try:
    codecs.lookup("mbcs")
except LookupError:
    ascii = codecs.lookup("ascii")
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == "mbcs"))

VERSION = "1.1.8"
URL = "https://github.com/xeroc/python-graphenelib"

setup(
    name="graphenelib",
    version=VERSION,
    description="Python library for graphene-based blockchains",
=======
VERSION = "0.1.1"
URL = "https://gitlab.pixelplex.by/645.echo/echopy-lib" # FIX IT
current_python_version = sys.version[:5]
current_requirements_file = "extended_requirements.txt" if int(current_python_version[0]) == 2 or int(current_python_version[2]) <= 5 else "requirements.txt"
packages = find_packages()
packages.remove('test')

setup(
    name="echopy-lib",
    version=VERSION,
    description="Python library for ECHO blockchain",
>>>>>>> develop
    long_description=open("README.md").read(),
    download_url="{}/tarball/{}".format(URL, VERSION), # FIX IT
    license='MIT',
    author="PixelPlex inc",
    author_email="dev@pixelplex.io",
    url=URL,
<<<<<<< HEAD
    keywords=["graphene", "api", "rpc", "ecdsa", "secp256k1"],
    packages=["grapheneapi", "graphenebase", "graphenestorage", "graphenecommon"],
=======
    keywords=["echo", "blockchain", "api", "rpc"],
    packages=packages,
>>>>>>> develop
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
<<<<<<< HEAD
        "Development Status :: 5 - Production/Stable",
=======
        "Development Status :: 4 - Beta",
>>>>>>> develop
        "Intended Audience :: Developers",
    ],
    install_requires=open(current_requirements_file).readlines(),
    include_package_data=True,

)
