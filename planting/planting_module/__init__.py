#!/usr/bin/env python
# encoding: utf-8
from abc import ABCMeta, abstractmethod
from environment import Environment
from planting_api_v1 import PlantingApi

class ModuleBase(metaclass=ABCMeta):
    def __init__(self):
        self._tasks = None

    @abstractmethod
    def register_machine(self, machine):
        pass
    
    def play(self):
        self.build_tasks()
        self._planting.run_planting([self._env.ip], self._tasks)
        self._planting.print_info()
        self._planting.clear_callback()

    @abstractmethod
    def build_tasks(self):
        pass
