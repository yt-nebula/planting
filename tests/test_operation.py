#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import tempfile

from planting.machine import Machine


def test_create(machine: Machine):
    assert True is machine.create(path="~/test1", state="dir")
    assert True is machine.shell(command="cd ~/test1")

    assert True is machine.create(path="~/test2", state="touch")
    assert True is machine.shell(command="cat ~/test2")


def test_copy(machine: Machine):
    with tempfile.NamedTemporaryFile() as f:
        f.write(b'Hello World!')
        f.seek(0)
        assert True is machine.copy(src=f.name, dest="/root/test.txt")
    assert True is machine.shell(command="cat /root/test.txt")
    assert True is machine.shell(command="mv /root/test.txt /root/temp")


def test_fetch(machine: Machine):
    assert True is machine.shell(command='''echo "Hello" >> ~/1.txt''')
    with tempfile.TemporaryDirectory() as tmpDir:
        assert True is machine.fetch(src="/root/1.txt", dest=tmpDir)
        res = os.popen('cat ' + tmpDir + "/" +
                       machine.ip + "/root/1.txt").read()
        print(res)
        assert res is not ""


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
