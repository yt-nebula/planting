#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Pip(ModuleBase):
    def __init__(self):
        super(Pip, self).__init__()

    def build_tasks(self, package, executable):
        self._tasks = [dict(
            action=dict(
                module='pip',
                args=dict(name=package, executable=executable))
        )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.pip = self

    def __call__(self, package, executable):
        self.build_tasks(package, executable)
        return self.play()
