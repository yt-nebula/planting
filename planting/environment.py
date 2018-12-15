#!/usr/bin/env python
# -*- coding: utf8 -*-


class Environment(object):
    def __init__(self, **kwargs):
        self.ssh_pass = kwargs['ssh_pass']
        self.ssh_user = kwargs['ssh_user']
        self.ip = kwargs['ip']
        self.python = '/usr/bin/python'
        if 'python' in kwargs:
            self.python = kwargs['python']
