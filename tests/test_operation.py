#!/usr/bin/env python
# encoding: utf-8
from planting.machine import Machine


def test_create(machine: Machine):
    machine.create(path="~/test", state="dir")
    assert True is machine.shell(command="cd ~/test")


def test_copy(machine: Machine):
    machine.create(path="~/test.txt", state="file")
    machine.copy(src="~/test.txt", dest="~/test_bak.txt")
    assert True is machine.shell(command="mv ~/test_bak.txt ~/temp")

# def test_create(machine: Machine):
#     machine.create(path="~/test", state="dir")
#     assert True is machine.shell(command="cd ~/test")

# def test_create(machine: Machine):
#     machine.create(path="~/test", state="dir")
#     assert True is machine.shell(command="cd ~/test")

# def test_create(machine: Machine):
#     machine.create(path="~/test", state="dir")
#     assert True is machine.shell(command="cd ~/test")