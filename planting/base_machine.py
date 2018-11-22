import sys


class Machine(object):
    def __init__(self):
        self._ip = None
        self._user = None
        self._password = None


class Cluster(object):
    def __init__(self):
        self.machines = []

    def add_machine(self, machine: Machine):
        self.machines.append(machine)
