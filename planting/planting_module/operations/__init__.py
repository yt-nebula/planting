#!/usr/bin/env python
# encoding: utf-8

import os
import pkgutil

from planting.environment import Environment
from planting.planting_module import ModuleBase
from planting.planting_api_v1 import PlantingApi

pkgpath = os.path.dirname(__file__)
pkgname = os.path.basename(pkgpath)

for _, file, _ in pkgutil.iter_modules([pkgpath]):
    __import__(pkgname+'.'+file)

