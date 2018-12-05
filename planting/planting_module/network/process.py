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

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "unarchive {0} to {1} success".format(self._src, self._dest))
        else:
            self._planting.logger.error("unarchive failed!")

    def active_state(self, planting):
        for host in planting.results_callback.host_ok:
            for task in planting.results_callback.host_ok[host]:
                return task['status']['ActiveState']
