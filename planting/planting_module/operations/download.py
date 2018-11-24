#!/usr/bin/env python
# encoding: utf-8

from environment import Environment
from planting_module import ModuleBase
from planting_api_v1 import PlantingApi
from machine import Machine


class Download(ModuleBase):
    def __init__(self):
        super(Download, self).__init__()

    def build_tasks(self):
        self._tasks = [dict(action=dict(
            module='get_url',
            url='http://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/MLbook2016-HowToUse.pdf'),  # noqa
            dest="~/MLbook2016-HowToUse.pdf")]
        
    def register_machine(self, machine: Machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.download = self
