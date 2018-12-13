#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
from functools import reduce
import json
from collections import OrderedDict
import os
from planting.machine import Machine
import paramiko

EXAMPLES = r"""

    with FileConfig(node, 'root/foo.conf') as src:

        src['ip'] = '196.168.0.1'
"""


class FileConfig(object):
    """Change a josn file on the remote machie

    Args:
        path(str): path of a file
        machine(str): an object of planting.machine.Machine

    """
    def __init__(self, machine, path):
        self._tasks = None
        self._env = machine._env
        self._path = path

    def get_content(self):
        self.ssh_client = FileConfigClient(self._env).ssh_client()
        self.remote_file = self.ssh_client.file(self._path, mode='r+')
        self.content = self.remote_file.read().decode('utf8')
        self.remote_file.close()
        return self.content

    def __enter__(self):
        self.src = self.get_content()
        self.src = json.loads(self.src)
        return self.src

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remote_temp_file = self.ssh_client.file(self._path, mode='w+')
        self.remote_temp_file.write(json.dumps(self.src, indent=4, sort_keys=False))
        self.remote_temp_file.close()

    def __setitem__(self, key, val):
        self.src[key] = val

    def __getitem__(self, item):
        self.src[item]


class Cont(str):
    def __init__(self, cont):
        self.str = cont


class FileConfigClient(object):

    def __init__(self, env):
        self._ip = env.ip
        self._user = env.remote_user
        self._pass = env.password

    def ssh_client(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname='10.40.50.132', username='linuxadmin', password='Hello=111!')

        return self.ssh.open_sftp()

if __name__ == '__main__':

    node = Machine('xxx', 'xxx', 'xxx', python='/usr/bin/python')
    with FileConfig(node, '/root/foo.conf') as src:

        src['ip'] = '196.168.0.1'