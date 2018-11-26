#!/usr/bin/env python
# encoding: utf-8

from planting_module import ModuleBase


class Remove(ModuleBase):
    def __init__(self):
        super(Remove, self).__init__()

    def build_tasks(self, src):
        self._tasks = [dict(
            action=dict(
                module='shell',
                args='rm -rf ' + src)
        )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.remove = self

    def __call__(self, src):
        self.build_tasks(src)
        return self.play()
