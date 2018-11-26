#!/usr/bin/env python
# encoding: utf-8

import sys

class Environment(object):
    def __init__(self, ip=None, remote_user=None, password=None):
        self.password = password
        self.remote_user = remote_user
        self.ip = ip
