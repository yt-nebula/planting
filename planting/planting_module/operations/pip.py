#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Pip(ModuleBase):
    """

    install python package

    Args:
        package(str): package name
        executable(str): pip version such as pip-3.3
    """
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

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "host {}: ".format(self._env.ip) +
                "pip install {0} success".format(self._package))
        else:
            self._planting.logger.error("install failed!")

    def __call__(self, package, executable):
        self.build_tasks(package, executable)
        self._package = package
        return self.play()
