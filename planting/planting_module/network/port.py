#!/usr/bin/env python
# encoding: utf-8

from environment import Environment
from planting_module import ModuleBase
from planting_api_v1 import PlantingApi


class Port(ModuleBase):
    def __init__(self):
        super(Port, self).__init__()

    def build_tasks(self, port):
        self._tasks = [dict(action=dict(
            module='port',
            args=port))]

    def output_field(self):
        self._output = 'msg'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.port = self

    def __call__(self, port):
        self.build_tasks(port)
        self.play()
