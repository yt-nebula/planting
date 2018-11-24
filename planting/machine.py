from planting_api_v1 import PlantingApi
from environment import Environment
from planting_module import operations


class Machine(object):
    def __init__(self, ip=None, remote_user=None, password=None):
        self._env = Environment(
            ip=ip, remote_user=remote_user, password=password)
        self.build_planting()
        self.modules = []

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


if __name__ == '__main__':
    node1 = Machine('127.0.0.1', 'aaaa', 'aaaaaa')
    node1.register(operations.download.Download)
    node1.register(operations.move.Move)
    node1.list_all_module()
    node1.move(src="~/test.py", dest="~/Music/test.py")
