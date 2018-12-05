#!/usr/bin/env python
# -*- coding: utf8 -*-
from planting.planting_module import ModuleBase


class Process(ModuleBase):
    """

    restarted, started or stopped the process

    Args:
        process(str): process number

        state(str): restarted, started or stopped

    Return:
        result(bool): execution status
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
        self._output = 'status'

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.process = self

    def __call__(self, process, state):
        self.build_tasks(process, state)
        self._planting.run_planting([self._env.ip], self._tasks)
        self.print_info(self._planting)
        return self._planting.result()

    def print_info(self, planting):
        for host in planting.results_callback.host_ok:
            for task in planting.results_callback.host_ok[host]:
                planting.logger.info(
                    host + ": " + str(task['status']['ActiveState']))

        for host in planting.results_callback.host_unreachable:
            for task in planting.results_callback.host_unreachable[host]:
                planting.logger.error(host + ": " + task['msg'])

        for host in planting.results_callback.host_failed:
            for task in planting.results_callback.host_failed[host]:
                planting.logger.error(host + ": " + task['msg'])
