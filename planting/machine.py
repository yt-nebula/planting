import sys
from planting_api_v1 import PlantingApi
from environment import Environment
from planting_module import ModuleBase
from planting_module import operations

class Machine(object):
    def __init__(self, ip=None, remote_user=None, password=None):
        self._env = Environment(
            ip=ip, remote_user=remote_user, password=password)
        self.modules = {}

    def build_planting(self):
        env = self._env
        if env.ip is None:
            raise AttributeError("missing parameter ip")
        if env.password is None:
            raise AttributeError("missing parameter password")
        if env.remote_user is None:
            raise AttributeError("missing parameter remote_user")
        self._planting = PlantingApi(self.env)

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
        for module, _ in self.modules.items():
            print(module)

    def register(self, module: ModuleBase):
        moduleName = type(module).__name__
        self.modules[moduleName] = module
        module.register_planting(self._planting)

if __name__ == '__main__':
    machine = Machine()
    machine.register(operations.download)

