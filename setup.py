#!/usr/bin/env python3
# -*- Coding: UTF-8 -*-
import os
from setuptools import setup, find_packages


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="rnae",
    license="Apache License 2.0",
    version='1.0.1',
    author='Allan F Souza',
    author_email='allanfdsz@gmail.com',
    packages=find_packages("src"),
    package_dir={"":"src"},
    description="Rede Neural Artifical Evolucionária",
    package_data={"":["dados/*.csv"]},
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="",
    include_package_data=True,
    zip_safe=False,
    install_requires=["numpy",
                      "pygenec"
                      ]
)
