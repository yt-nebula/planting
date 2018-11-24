#!/usr/bin/env python
# encoding: utf-8

from environment import Environment
from planting_module import ModuleBase
from planting_api_v1 import PlantingApi


class Create(ModuleBase):
    def __init__(self):
        super(Create, self).__init__()

    def build_tasks(self, path: str, state: str):
        command = state is "dir" and "mkdir" or "touch"
        self._tasks = [dict(
            action=dict(
                module='shell',
                args=command + ' ' + path)
        )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.create = self

    def __call__(self, path, state):
        self.build_tasks(path, state)
        return self.play()
