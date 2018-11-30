#!/usr/bin/env python
# -*- coding: utf8 -*-


class Environment(object):
    def __init__(self, **kwargs):
        self.password = kwargs['password']
        self.remote_user = kwargs['remote_user']
        self.ip = kwargs['ip']
        self.python = '/usr/bin/python'
        if 'python' in kwargs:
            self.python = kwargs['python']
