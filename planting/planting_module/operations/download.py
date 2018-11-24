from environment import Environment
from planting_module import ModuleBase
from planting_api_v1 import PlantingApi
from machine import Machine


class Download(ModuleBase):
    def __init__(self):
        super(Download, self).__init__()

    def build_tasks(self, url, dest):
        self._tasks = [dict(action=dict(
            module='get_url',
            args=dict(url=url, dest=dest)))]

    def output_field(self):
        self._output = 'msg'

    def register_machine(self, machine: Machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.download = self

    def register_machine(self, machine: Machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.download = self

    def __call__(self, url, dest):
        self.build_tasks(url, dest)
        self.play()
