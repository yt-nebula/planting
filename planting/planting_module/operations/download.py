#!/usr/bin/env python
# encoding: utf-8

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
        
    def register_machine(self, machine: Machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.download = self

    def output_field(self, field):
        self._output = field

    def __call__(self):
        self.build_tasks(url, dest)
        self.output_field('msg')
        self.play()

