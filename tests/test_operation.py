#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import re
import tarfile
import logging
import tempfile

import pytest

from planting.exception import AnsibleFailException
from planting.machine import Machine


def test_copy(machine: Machine):
    with tempfile.NamedTemporaryFile() as f:
        f.write(b'Hello World!')
        f.seek(0)
        assert True is machine.copy(src=f.name, dest="/root/test.txt")
    assert True is machine.shell(command="cat /root/test.txt")
    assert True is machine.shell(command="mv /root/test.txt /root/temp")


def test_copy_file_not_found(machine: Machine):
    logger = logging.getLogger('console')
    with tempfile.NamedTemporaryFile() as f:
        f.write(b'Hello World!')
        f.seek(0)
        with pytest.raises(AnsibleFailException) as ex:
            machine.copy(src="xxxx.txt", dest="/root/test.txt")
        logger.error(ex)


def test_create(machine: Machine):
    assert True is machine.create(path="~/test1", state="dir")
    assert True is machine.shell(command="cd ~/test1")

    assert True is machine.create(path="~/test2", state="touch")
    assert True is machine.shell(command="cat ~/test2")


def test_download(machine: Machine):
    assert True is machine.download(
        url="http://www.runoob.com/wp-content/uploads/"
        "2015/10/vi-vim-cheat-sheet-sch.gif",
        dest="~/vim.gif")
    assert True is machine.shell(command="mv ~/vim.gif ~/test.gif")


def test_fetch(machine: Machine):
    assert True is machine.shell(command='''echo "Hello" >> ~/1.txt''')
    with tempfile.TemporaryDirectory() as tmpDir:
        assert True is machine.fetch(src="/root/1.txt", dest=tmpDir)
        res = os.popen('cat ' + tmpDir + "/" +
                       machine.ip + "/root/1.txt").read()
        assert res is not ""


def test_move(machine: Machine):
    assert True is machine.create(path="~/test", state="file")
    assert True is machine.move(src="~/test", dest="~/move")
    assert True is machine.shell(command="mv ~/move ~/foo")


def test_remove(machine: Machine):
    logger = logging.getLogger('console')
    assert True is machine.create(path="~/test", state="file")
    assert True is machine.remove(src="~/test")
    with pytest.raises(AnsibleFailException) as ex:
        assert False is machine.shell(command="mv ~/test ~/test.txt")
    logger.error(ex)


def test_pip(machine: Machine):
    assert True is machine.pip(package="six")
    assert True is machine.shell(command="pip show six")
    msg = machine.shell.success_message()
    pattern = re.compile(r"Name: six")
    assert pattern.findall(msg) is not 0


def test_waitfor(machine: Machine):
    assert True is machine.wait_for(port='22', state='started', timeout=10)
    # FIXME: can't test close port due to missing nginx
    # machine.shell(command='nginx -c /usr/local/nginx/conf/nginx.conf')
    # assert True is machine.wait_for(port='80', state='started', timeout=10)


def test_unarchive(machine: Machine):
    f = tempfile.NamedTemporaryFile(prefix='test', suffix='tar', delete=True)
    f.write(b'Hello World!')
    f.seek(0)
    # compress file
    with tarfile.open("test.tar.gz", "w:gz") as tar:
        tar.add(f.name)
    assert True is machine.unarchive(src=tar.name, dest="/root/")
    f.close()
    assert True is machine.shell(command="cat /root/tmp/test*tar")
    # FIXME: can't test in docker due to missing systemctl or service
    # def test_process(machine: Machine):
    # assert True is machine.process(process="rsync", state="started")
    # assert True is machine.shell(command="service rsync status")
