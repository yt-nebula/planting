#!/usr/bin/env python
# encoding: utf-8

from planting_module import ModuleBase


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

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.shell = self

    def __call__(self, command):
        self.build_tasks(command)
        return self.play()
