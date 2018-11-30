#!/usr/bin/env python
# -*- coding: utf8 -*-
from planting.machine import Machine


def test_create(machine: Machine):
    assert True is machine.create(path="~/test1", state="dir")
    assert True is machine.shell(command="cd ~/test1")

    assert True is machine.create(path="~/test2", state="touch")
    assert True is machine.shell(command="cat ~/test2")


def test_copy(machine: Machine):
    assert True is machine.create(path="~/test.txt", state="file")
    assert True is machine.copy(src="~/test.txt",
                                dest="~/test_bak.txt", remote_src="yes")
    assert True is machine.shell(command="mv ~/test_bak.txt ~/temp")


def test_download(machine: Machine):
    assert True is machine.download(
        url="http://www.runoob.com/wp-content/uploads/"
        "2015/10/vi-vim-cheat-sheet-sch.gif",
        dest="~/vim.gif")
    assert True is machine.shell(command="mv ~/vim.gif ~/test.gif")


def test_move(machine: Machine):
    assert True is machine.create(path="~/test", state="file")
    assert True is machine.shell(command="ls")
    assert True is machine.move(src="~/test", dest="~/move")
    assert True is machine.shell(command="mv ~/move ~/foo")
