#!/usr/bin/env python
# -*- coding: utf8 -*-
from planting.planting_module import ModuleBase


class Process(ModuleBase):
    """

    restarted, started or stopped the process

    Args:
        process(str): process number
        state(str): restarted, started or stopped
    """
    def __init__(self):
        super(Process, self).__init__()

    def build_tasks(self, process, state):
        self._tasks = [dict(
            action=dict(
                module='service',
                args=dict(name=process, state=state))
        )]

    def output_field(self):
        self._output = 'changed'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.process = self

    def __call__(self, process, state):
        self.build_tasks(process, state)
        self.play()
