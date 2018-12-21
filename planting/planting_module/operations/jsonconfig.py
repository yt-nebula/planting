#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
os.sys.path.append('/home/jlpan/github/planting/')
import os
from functools import reduce
import json
import logging
from collections import OrderedDict
import os
import paramiko

EXAMPLES = r"""

    with JsonConfig(node, 'root/foo.conf') as src:

        src['ip'] = '196.168.0.1'
"""

FormatError = json.decoder.JSONDecodeError

class JsonConfig(object):
    """Change a josn file on the remote machie

    Args:
        path(str): path of a file
        machine(str): an object of planting.machine.Machine

    """
    def __init__(self, machine, path):
        self._tasks = None
        self._env = machine._env
        self._path = path
        self._planting = machine._planting
        self.logger = logging.getLogger('console')

    def get_content(self):
        self.ssh_client = self.create_connect()
        self.remote_file = self.ssh_client.file(self._path, mode='r+')
        self.content = self.remote_file.read().decode('utf8')
        self.remote_file.close()
        return self.content

    def create_connect(self):
        return JsonConfigClient(self._env).ssh_client()

    def __enter__(self):
        self.src = self.get_content()
        try:
            self.src = json.loads(self.src)
        except FormatError:
            self.logger_info('{} is not json file'.format(self._path))
        return self.src

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger_info("host {}: ".format(self._env.ip) +
                        "Configure {0} Successfully".format(self._path))
        self.remote_temp_file = self.ssh_client.file(self._path, mode='w+')
        self.remote_temp_file.write(json.dumps(self.src, indent=4, sort_keys=False))
        self.remote_temp_file.close()    

    def logger_info(self, msg):
        self.logger.info(msg)

    def __setitem__(self, key, val):
        self.src[key] = val

    def __getitem__(self, item):
        self.src[item]

class JsonConfigClient(object):

    def __init__(self, env):
        self._ip = env.ip
        self._user = env.remote_user
        self._pass = env.password

    def ssh_client(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname=self._ip, username=self._user, password=self._pass)
        return self.ssh.open_sftp()

if __name__ == '__main__':

    node = Machine('xxx', 'xxx', 'xxx', python='/usr/bin/python')
    with JsonConfig(node, '/root/foo.conf') as src:

        src['ip'] = '196.168.0.1'