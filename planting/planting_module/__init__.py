#!/usr/bin/env python
# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod

from planting.exception import AnsibleFailException, AnsibleUnreachableException


class ModuleBase(metaclass=ABCMeta):
    def __init__(self):
        self._tasks = None
        self._env = None
        self._planting = None

    @abstractmethod
    def register_machine(self, machine):
        pass

    @abstractmethod
    def build_tasks(self):
        pass

    @abstractmethod
    def __call__(self):
        pass

    @abstractmethod
    def print_info(self):
        pass

    def handle_exception(self):
        failed = self._planting.failed_message()
        unreachable = self._planting.unreachable_message()
        if failed is not "":
            raise AnsibleFailException(failed)
        if unreachable is not "":
            raise AnsibleUnreachableException(unreachable)

    def play(self) -> bool:
        self._planting.run_planting([self._env.ip], self._tasks)
        self.handle_exception()
        self.print_info()
        return self._planting.result()
