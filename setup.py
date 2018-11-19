#!/usr/bin/env python
# -*- coding: utf8 -*-

from setuptools import setup, find_packages

__version__ = "1.0.0"

setup(
    name='plantingtest',
    version=__version__,
    description="a deploy tool for ficus",
    long_description='',
    classifiers=[
        
    ], 
    keywords='',
    author='',
    author_email='',
    url='https://github.com/yt-nebula/planting.git',
    license='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['ansible==2.3.2.0',
                    'paramiko==2.2.1',
                    'colorama',
                    'tqdm',
                    'retrying',
                    'jinja2',
                    'fabric==1.14.0'],
    entry_points={
        'PLANTING':[
            'PLUGIN=opod_deploy_plugin.plugin: OpodDeployPlugin'
    ]
    },
)