#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import re
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
    assert True is machine.move(src="~/test", dest="~/move")
    assert True is machine.shell(command="mv ~/move ~/foo")


def test_remove(machine: Machine):
    assert True is machine.create(path="~/test", state="file")
    assert True is machine.remove(src="~/test")
    assert False is machine.shell(command="mv ~/test ~/test.txt")


def test_pip(machine: Machine):
    assert True is machine.pip(package="six", executable="/root/venv/bin/pip")
    assert True is machine.shell(command="/root/venv/bin/pip show six")
    msg = machine.shell.success_message()
    pattern = re.compile(r"Name: six")
    assert pattern.findall(msg) is not 0


def test_jsoninfile(machine: Machine):
    template_raw = b'''{
    "master":{
        "id": 1,
        "ip": "xxx",
        "usr": ["a", "b"]
    }
}
'''
    template_change = b'''{
    "master":{
        "id": 2,
        "ip": "xxx",
        "usr": ["a", "b"]
    }
}
'''
    with tempfile.NamedTemporaryFile() as f:
        f.write(template_raw)
        f.seek(0)
        assert True is machine.copy(src=f.name, dest="~/test_raw")
    assert True is machine.jsoninfile(path="~/test_raw",
                                      keys=["master", "id"], val=2)

    with tempfile.NamedTemporaryFile() as f:
        f.write(template_change)
        f.seek(0)
        assert True is machine.copy(src=f.name, dest="~/test_change")

    assert True is machine.shell(command="jq '.master|.id' ~/test_raw > ~/awf")
    assert True is machine.shell(
        command="jq '.master|.id' ~/test_change > ~/bxg")

    assert True is machine.shell(command="diff ~/awf ~/bxg > ~/diffjson")

    with tempfile.TemporaryDirectory() as tmpDir:
        assert True is machine.fetch(src="/root/diffjson", dest=tmpDir)
        res = os.popen('cat ' + tmpDir + "/" +
                       machine.ip + "/root/diffjson").read()
        print(res)
        assert res is ""

# FIXME: can't test in docker due to missing GNU tar
# def test_unarchive(machine: Machine):
#     f = tempfile.NamedTemporaryFile()
#     f.write(b'Hello World!')
#     f.seek(0)
#     # compress file
#     with tarfile.open("test.tar.gz", "w:gz") as tar:
#         tar.add(f.name)
#     assert True is machine.unarchive(src=tar.name, dest="/root/")
#     f.close()
