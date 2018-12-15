#!/usr/bin/env python
# -*- coding: utf8 -*-

import inspect

from planting.planting_api_v1 import PlantingApi
from planting.environment import Environment
from planting.planting_module import ModuleBase
from planting.planting_module import operations, network


class Machine(object):
    """

    Class Machine

    Args:
        ip(str): host

        ssh_user(str): ssh username

        ssh_pass(str): ssh password

    """
    def __init__(self, ip=None, ssh_user=None, ssh_pass=None, **kwargs):
        # FIXME: remove python parameter when docker image fix
        if 'python' not in kwargs:
            kwargs['python'] = '/usr/bin/python'
        self._env = Environment(
            ip=ip,
            remote_user=ssh_user,
            password=ssh_pass,
            python=kwargs['python'])
        self.build_planting()
        self.modules = []

    def register_all(self):
        self.register_from_module(operations)
        self.register_from_module(network)

    def register_from_module(self, module):
        for name, obj in inspect.getmembers(module):
            if inspect.ismodule(obj):
                for name, obj in inspect.getmembers(obj):
                    if inspect.isclass(obj) and not inspect.isabstract(obj):
                        if issubclass(obj, ModuleBase):
                            self.register(obj)

    def build_planting(self):
        env = self._env
        if env.ip is None:
            raise AttributeError("missing parameter ip")
        if env.ssh_pass is None:
            raise AttributeError("missing parameter password")
        if env.ssh_user is None:
            raise AttributeError("missing parameter remote_user")
        self._planting = PlantingApi(env)

    @property
    def password(self):
        return self._env.ssh_pass

    @password.setter
    def password(self, value):
        self._env.ssh_pass = value

    @property
    def remote_user(self):
        return self._env.ssh_user

    @remote_user.setter
    def remote_user(self, value):
        self._env.ssh_user = value

    @property
    def ip(self):
        return self._env.ip

    @ip.setter
    def ip(self, value):
        self._env.ip = value

    def list_all_module(self):
        for module in self.modules:
            print(module)

    def register(self, moduleClass):
        moduleName = moduleClass.__name__
        self.modules.append(moduleName)
        module = moduleClass()
        module.register_machine(self)
