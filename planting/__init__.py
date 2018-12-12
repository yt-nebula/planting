#!/usr/bin/env python
# -*- coding: utf8 -*-

import os

import logging.config

from planting.logger import LOGGING

os.makedirs('logs', exist_ok=True)
logging.config.dictConfig(LOGGING)
