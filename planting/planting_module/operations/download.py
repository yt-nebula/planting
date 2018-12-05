#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Download(ModuleBase):
    """

    download file

    Args:
        url(str): source file

        dest(str): destination path
    """
    def __init__(self):
        super(Download, self).__init__()

    def build_tasks(self, url, dest):
        self._tasks = [dict(action=dict(
            module='get_url',
            args=dict(url=url, dest=dest)))]

    def output_field(self):
        self._output = 'msg'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.download = self

    def __call__(self, url, dest):
        self.build_tasks(url, dest)
        return self.play()
