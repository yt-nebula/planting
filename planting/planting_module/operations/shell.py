#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Shell(ModuleBase):
    """

    execute bash command

    Args:
        command(str): bash command

    Return:
        result(bool): execution status
    """
    def __init__(self):
        super(Shell, self).__init__()

    def build_tasks(self, command):
        self._tasks = [dict(
            action=dict(
                module='shell',
                args=command)
        )]

    def get_output(self):
        self._planting.results_callback

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.shell = self

    def success_message(self):
        return self._planting.success_message('stdout')

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "host {}: ".format(self._env.ip) +
                "execute \"{}\" success!".format(self._command))
        else:
            self._planting.print_error()

    def __call__(self, command) -> bool:  # type: ignore
        self.build_tasks(command)
        self._command = command
        return self.play()
