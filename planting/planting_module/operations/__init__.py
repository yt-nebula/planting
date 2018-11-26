#!/usr/bin/env python
# encoding: utf-8

import os
import pkgutil

pkgpath = os.path.dirname(__file__)
pkgname = os.path.basename(pkgpath)

for _, file, _ in pkgutil.iter_modules([pkgpath]):
    __import__('planting_module.' + pkgname+'.'+file)
