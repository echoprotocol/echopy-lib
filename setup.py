#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import sys

VERSION = "0.1.3"
packages = find_packages()
packages.remove('test')

setup(
    name="echopy-lib",
    version=VERSION,
    description="Python library for ECHO blockchain",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    download_url="https://pypi.python.org/pypi/echopy-lib",
    license='MIT',
    author="PixelPlex inc",
    author_email="dev@pixelplex.io",
    url="https://echo-dev.io/",
    keywords=["echo", "blockchain", "api", "rpc"],
    packages=packages,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    install_requires=open("requirements.txt").readlines(),
    include_package_data=True,

)
