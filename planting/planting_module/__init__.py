#!/usr/bin/env python
# -*- coding: utf8 -*-
from abc import ABCMeta, abstractmethod


class ModuleBase(metaclass=ABCMeta):
    def __init__(self):
        self._tasks = None
        self._output = None

    @abstractmethod
    def register_machine(self, machine):
        pass

    @abstractmethod
    def output_field(self):
        pass

    @abstractmethod
    def build_tasks(self):
        pass

    @abstractmethod
    def __call__(self):
        pass

    def play(self):
        self.output_field()
        self._planting.run_planting([self._env.ip], self._tasks)
        self._planting.print_info(self._output)
        return self._planting.result()
