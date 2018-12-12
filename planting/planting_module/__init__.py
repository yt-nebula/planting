#!/usr/bin/env python
# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod


class ModuleBase(metaclass=ABCMeta):
    def __init__(self):
        self._tasks = None

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

    def play(self):
        self._planting.run_planting([self._env.ip], self._tasks)
        self.print_info()
        return self._planting.result()
