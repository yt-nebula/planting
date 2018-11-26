#!/usr/bin/env python
# encoding: utf-8

from planting_module import ModuleBase


class Pip(ModuleBase):
    def __init__(self):
        super(Pip, self).__init__()

    def build_tasks(self, package):
        self._tasks = [dict(
            action=dict(
                module='shell',
                args='pip install ' + package)
        )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.pip = self

    def __call__(self, package):
        self.build_tasks(package)
        self.play()
