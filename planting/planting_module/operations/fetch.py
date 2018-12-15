#!/usr/bin/env python
# -*- coding: utf8 -*-
from planting.planting_module import ModuleBase


class Fetch(ModuleBase):
    """

    copy files from remote machine to local machine

    Args:
        src(str): remote path

        dest(str): local path

    Return:
        result(bool): execution status
    """
    def __init__(self):
        super(Fetch, self).__init__()

    def build_tasks(self, src, dest):
        self._tasks = [dict(action=dict(
            module='fetch',
            args=dict(src=src, dest=dest)))]

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.fetch = self

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "host {}: ".format(self._env.ip) +
                "fetch from remote {0} to local {1} success!"
                .format(self._src, self._dest))
        else:
            self._planting.print_error()

    def __call__(self, src, dest) -> bool:  # type: ignore
        self.build_tasks(src, dest)
        self._src, self._dest = src, dest
        return self.play()
