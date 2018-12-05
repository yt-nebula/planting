#!/usr/bin/env python
# -*- coding: utf8 -*-
from planting.planting_module import ModuleBase


class WaitFor(ModuleBase):
    """

    wait for the port until started or stopped

    Args:
        port(str): port number

        state(str): started or stopped

        timeout(int): the number of timeout

    Return:
        result(bool): execution status
    """
    def __init__(self):
        super(WaitFor, self).__init__()

    def build_tasks(self, port, state, timeout=30):
        self._tasks = [dict(
            action=dict(
                module='wait_for',
                args=dict(port=port, state=state, timeout=timeout))
        )]

    def output_field(self):
        self._output = 'msg'

    def get_output(self):
        self._planting.results_callback

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.wait_for = self

    def __call__(self, port, state, timeout):
        self.build_tasks(port, state, timeout)
        self._planting.run_planting([self._env.ip], self._tasks)
        return self._planting.result()
