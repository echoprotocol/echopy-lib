#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

VERSION = "0.1.0"
URL = "https://gitlab.pixelplex.by/645.echo/echopy-lib" # FIX IT

setup(
    name="echopy-lib",
    version=VERSION,
    description="Python library for ECHO blockchain",
    long_description=open("README.md").read(),
    download_url="{}/tarball/{}".format(URL, VERSION), # FIX IT
    license='MIT',
    author="PixelPlex inc",
    author_email="dev@pixelplex.io",
    url=URL,
    keywords=["echo", "blockchain", "api", "rpc"],
    packages=["echoapi", "echobase", "echo"],
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
