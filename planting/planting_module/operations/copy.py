#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Copy(ModuleBase):
    def __init__(self):
        super(Copy, self).__init__()

    def build_tasks(self, src, dest, remote_src):
        self._tasks = [dict(action=dict(
            module='copy',
            args=dict(src=src, dest=dest, remote_src=remote_src)))]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.copy = self

    def __call__(self, src, dest, remote_src):
        self.build_tasks(src, dest, remote_src)
        return self.play()
