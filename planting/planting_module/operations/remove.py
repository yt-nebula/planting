#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Remove(ModuleBase):
    """

    delete file or directory

    Args:
        src(str): source file
    """
    def __init__(self):
        super(Remove, self).__init__()

    def build_tasks(self, src):
        self._tasks = [dict(
            action=dict(
                module='shell',
                args='rm -rf ' + src)
        )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.remove = self

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "remove {0} success".format(self._src))
        else:
            self._planting.logger.error("remove failed!")

    def __call__(self, src):
        self.build_tasks(src)
        self._src = src
        return self.play()
