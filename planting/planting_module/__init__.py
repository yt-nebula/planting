#!/usr/bin/env python
# encoding: utf-8
from abc import ABCMeta, abstractmethod
from environment import Environment
from planting.planting_api_v1 import PlantingApi


class ModuleBase(metaclass=ABCMeta):
    def __init__(self, env: Environment):
        self._env = env

    def register_planting(self, planting: PlantingApi):
        self._planting = planting

    @abstractmethod
    def _play():
        pass
