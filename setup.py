#!/usr/bin/env python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages


package_name = "planting"
packages = find_packages(
    include=[package_name, "{}.*".format(package_name)]
)

setup(
    name="Planting",
    version="1.0.a",
    description='Next generation deployment tool fully depended on Ansible.',
    license='BSD License',
    packages=packages,
    platforms=["all"],
    url='https://github.com/yt-nebula/planting',
    install_requires=[
        'ansible==2.5.0',
        'colorama',
    ],
    classifiers=[
        "Operating System :: linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ]
)
