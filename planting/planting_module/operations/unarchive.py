#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Unarchive(ModuleBase):
    """

    unarchive file

    Args:
        src(str): source file path

        dest(str): destination file

    Return:
        result(bool): execution status
    """
    def __init__(self):
        super(Unarchive, self).__init__()

    def build_tasks(self, src, dest):
        self._tasks = [dict(
            action=dict(
                module='unarchive',
                args=dict(src=src, dest=dest))
        )]

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.unarchive = self

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "host {}: ".format(self._env.ip) +
                "unarchive {0} to {1} success".format(self._src, self._dest))
        else:
            self._planting.print_error()

    def __call__(self, src, dest):
        self.build_tasks(src, dest)
        self._src, self._dest = src, dest
        return self.play()
