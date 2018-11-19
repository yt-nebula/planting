#!/usr/bin/env python
# encoding: utf-8

import json
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase

Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'remote_user',
                                'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                                'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check',
                                'diff'])

# return the command result
class ResultCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

        # level = self._logger.DEBUG
        # complete_log = []
        # import time
        # f = open('ansible_debug_{time}.log'.format(
        #             time=time.strftime(
        #                 '%Y_%m_%d', time.localtime(
        #                     time.time()))), 'w')
        # self._logger.add_consumers(
        #     (self._logger.VERBOSE_DEBUG, f), (level, complete_log.append), )


    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class Planting(object):

    def __init__(self, machine, module_name, **kwargs):
        self.loader = DataLoader()
        self.options = Options(connection='smart', module_path=['/usr/share/ansible'], forks=100,
                        remote_user=None, private_key_file=None, ssh_common_args=None, ssh_extra_args=None,
                        sftp_extra_args=None, scp_extra_args=None, become=None, become_method=None,
                        become_user=None, verbosity=None, check=False, diff=False)

        self.inventory = InventoryManager(loader=self.loader, sources='hosts')
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        self.module_name = module_name
        self.host_list = machine
        self.module_args = kwargs
        self.passwords = dict()
        self.results_callback = ResultCallback()

    def run(self):
        play_source = dict(
            name="Planting Play",
            hosts=self.host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=self.module_name, args=self.module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords
            )
            tqm._stdout_callback = self.results_callback
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

        print("UP ***********")
        for host, result in self.results_callback.host_ok.items():
            print('{0} >>> {1}'.format(host, result._result))

        print("FAILED *******")
        for host, result in self.results_callback.host_failed.items():
            print('{0} >>> {1}'.format(host, result._result))

        print("DOWN *********")
        for host, result in self.results_callback.host_unreachable.items():
            print('{0} >>> {1}'.format(host, result._result))