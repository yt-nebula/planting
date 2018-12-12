#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Copy(ModuleBase):
    """

    copy file

    Args:
        src(str): source file path

        dest(str): destination path

    Return:
        result(bool): execution status
    """
    def __init__(self):
        super(Copy, self).__init__()

    def build_tasks(self, src, dest):
        self._tasks = [dict(action=dict(
            module='copy',
            args=dict(src=src, dest=dest, mode="preserve")))]

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.copy = self

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "host {}: ".format(self._env.ip) +
                "copy from {0} to {1} success".format(self._src, self._dest))
        else:
            self._planting.print_error()

    def __call__(self, src, dest):
        self.build_tasks(src, dest)
        self._src, self._dest = src, dest
        return self.play()
