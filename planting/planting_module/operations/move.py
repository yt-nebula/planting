#!/usr/bin/env python
# encoding: utf-8

from planting_module import ModuleBase


class Move(ModuleBase):
    def __init__(self):
        super(Move, self).__init__()

    def build_tasks(self, src, dest):
        self._tasks = [dict(
            action=dict(
                module='shell',
                args='mv ' + src + ' ' + dest)
        )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.move = self

    def __call__(self, src, dest):
        self.build_tasks(src, dest)
        self.play()
