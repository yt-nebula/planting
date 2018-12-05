#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Move(ModuleBase):
    """

    move file

    Args:
        src(str): source file path
        dest(str): destination path
    """

    def __init__(self):
        super(Move, self).__init__()

    def build_tasks(self, src, dest):
        self._tasks = [dict(
            action=dict(
                module='shell',
                args='mv ' + src + ' ' + dest)
        )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.move = self

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "move {0} to {1} success".format(self._src, self._dest))
        else:
            self._planting.logger.error("modify failed!")

    def __call__(self, src, dest):
        self.build_tasks(src, dest)
        self._src, self._dest = src, dest
        return self.play()
