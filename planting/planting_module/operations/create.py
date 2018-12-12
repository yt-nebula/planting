#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Create(ModuleBase):
    """

    create the file or directory

    Args:
        path(str): path of created file or directory

        state(str): create file when state = ‘file’，create directory when state = ‘dir’

    Return:
        result(bool): execution status
    """
    def __init__(self):
        super(Create, self).__init__()

    def build_tasks(self, path: str, state: str):
        command = state is "dir" and "mkdir" or "touch"
        self._tasks = [dict(
            action=dict(
                module='shell',
                args=command + ' ' + path)
        )]

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.create = self

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "host {}: ".format(self._env.ip) +
                "create {0} {1} success".format(self._state, self._path))
        else:
            self._planting.print_error()

    def __call__(self, path, state):
        self.build_tasks(path, state)
        self._path, self._state = path, state
        return self.play()
