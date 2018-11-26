import sys
import os
import pkgutil
import inspect

from planting_api_v1 import PlantingApi
from environment import Environment
from planting_module import ModuleBase
from planting_module import operations, network


class Machine(object):
    def __init__(self, ip=None, remote_user=None, password=None):
        self._env = Environment(
            ip=ip, remote_user=remote_user, password=password)
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
        if env.password is None:
            raise AttributeError("missing parameter password")
        if env.remote_user is None:
            raise AttributeError("missing parameter remote_user")
        self._planting = PlantingApi(env)

    @property
    def password(self):
        return self._env.password

    @password.setter
    def password(self, value):
        self._env.password = value

    @property
    def remote_user(self):
        return self._env.remote_user

    @remote_user.setter
    def remote_user(self, value):
        self._env.remote_user = value

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
