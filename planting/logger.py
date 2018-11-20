#!/usr/bin/env python
# encoding: utf-8
"""
@author: binshao
@file: planting_api_v1.py
"""
import json
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


Options = namedtuple('Options',
                     ['connection',
                      'remote_user',
                      'ask_sudo_pass',
                      'verbosity',
                      'ack_pass',
                      'module_path',
                      'forks',
                      'become',
                      'become_method',
                      'become_user',
                      'check',
                      'listhosts',
                      'listtasks',
                      'listtags',
                      'syntax',
                      'sudo_user',
                      'sudo',
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


class PlantingApi(object):
    def __init__(self):

        self.ops = Options(connection='smart',
                           remote_user=None,
                           ack_pass=None,
                           sudo_user=None,
                           forks=5,
                           sudo=None,
                           ask_sudo_pass=False,
                           verbosity=5,
                           module_path=None,
                           become=None,
                           become_method=None,
                           become_user=None,
                           check=False,
                           diff=False,
                           listhosts=None,
                           listtasks=None,
                           listtags=None,
                           syntax=None)
        self.loader = DataLoader()
        self.variable_manager = VariableManager()
        self.passwords = dict()
        self.results_callback = ResultCallback()
        # after ansible 2.3 need parameter 'sources'
        self.inventory = InventoryManager(loader=self.loader, sources='hosts')
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    def run_planting(self, host_list, module_name, module_args):
        play_source = dict(
            name="Planting Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.ops,
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


if __name__ == "__main__":
    planting_test = PlantingApi()
    hosts = ['10.40.40.183']
    
    src = 'http://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/MLbook2016-HowToUse.pdf'
    dest = '~/MLbook2016-HowToUse.pdf'
    args = {}
    args['url'] = src
    args['dest'] = dest

    planting_test.run_planting(hosts, 'get_url', args)
