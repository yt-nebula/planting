#!/usr/bin/env python
# encoding: utf-8

from planting.environment import Environment
from planting.planting_module import ModuleBase
from planting.planting_api_v1 import PlantingApi


class Download(ModuleBase):
    def __init__(self, env: Environment):
        super(Download, self).__init__(env)

    def _play(self):
        tasks = [ dict(action=dict(module='get_url', url='url')) ]
        planting_test.run_planting(hosts, tasks)
        planting_test.print_info()
        planting_test.clear_callback()
