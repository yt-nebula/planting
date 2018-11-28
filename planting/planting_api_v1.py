#!/usr/bin/env python
# encoding: utf-8
"""
@author: rfkimi
@file: planting_api_v1.py
"""
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.inventory.host import Host
from ansible.playbook.play import Play
from ansible.inventory.host import Host
from ansible.executor.task_queue_manager import TaskQueueManager

from collections import defaultdict
from callback_json import ResultCallback
from logger import logger
from environment import Environment

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


class PlantingApi(object):
    def __init__(self, env: Environment):
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
        self.passwords = {"conn_pass": env.password}
        self.results_callback = ResultCallback()
        self.logger = logger
        level = logger.DEBUG
        complete_log = []
        logger.add_consumers(
            (logger.VERBOSE_DEBUG, sys.stdout),
            (level, complete_log.append)
        )
        # after ansible 2.3 need parameter 'sources'
        # create inventory, use path to host config file
        # as source or hosts in a comma separated string
        self.inventory = InventoryManager(
            loader=self.loader, sources=env.ip+',')
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)
        host_info = Host(name=env.ip, port='22')
        self.variable_manager.set_host_variable(
            host_info, 'ansible_user', env.remote_user)
        self.variable_manager.set_host_variable(
            host_info, 'ansible_pass', env.password)

    def run_planting(self, host_list, task_list):
        play_source = dict(
            name="Planting Play",
            hosts=self.host_pattern,
            gather_facts='no',
            tasks=task_list
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
            self.clear_callback()
            tqm._stdout_callback = self.results_callback
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def print_info(self, field):
        for host in self.results_callback.host_ok:
            for task in self.results_callback.host_ok[host]:
                self.logger.info(host + ":\n" + str(task[field]))

        for host in self.results_callback.host_unreachable:
            for task in self.results_callback.host_unreachable[host]:
                self.logger.error(host + ":\n" + task['msg'])

        for host in self.results_callback.host_failed:
            for task in self.results_callback.host_failed[host]:
                self.logger.error(host + ":\n" + task['msg'])

    def clear_callback(self):
        self.results_callback.host_unreachable = defaultdict(list)
        self.results_callback.host_failed = defaultdict(list)
        self.results_callback.host_ok = defaultdict(list)
        self.results_callback.success = True

    def result(self):
        return self.results_callback.success
