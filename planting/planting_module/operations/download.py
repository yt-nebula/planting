#!/usr/bin/env python
# -*- coding: utf8 -*-

from planting.planting_module import ModuleBase


class Download(ModuleBase):
    """

    download file

    Args:
        url(str): source file

        dest(str): destination path

    Return:
        result(bool): execution status
    """
    def __init__(self):
        super(Download, self).__init__()

    def build_tasks(self, url, dest):
        self._tasks = [dict(action=dict(
            module='get_url',
            args=dict(url=url, dest=dest)))]

    def register_machine(self, machine):
        self._env = machine._env
        self._planting = machine._planting
        machine.download = self

    def print_info(self):
        res = self._planting.result()
        if res is True:
            self._planting.logger.info(
                "host {}: ".format(self._env.ip) +
                "download from url: {0} to {1} success"
                .format(self._url, self._dest))
        else:
            self._planting.print_error()

    def __call__(self, url, dest):
        self.build_tasks(url, dest)
        self._url, self._dest = url, dest
        return self.play()
