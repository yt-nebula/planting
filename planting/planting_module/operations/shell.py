#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Shell(ModuleBase):
    def __init__(self):
        super(Shell, self).__init__()

    def build_tasks(self, command):
        self._tasks = [dict(
            action=dict(
                module='shell',
                args=command)
        )]

    def output_field(self):
        self._output = 'stdout'

    def get_output(self):
        self._planting.results_callback

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.shell = self

    def success_message(self):
        return self._planting.success_message(self._output)

    def __call__(self, command):
        self.build_tasks(command)
        return self.play()
