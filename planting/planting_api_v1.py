#!/usr/bin/env python
# encoding: utf-8
"""
@author: rfkimi
@file: planting_api_v1.py
"""
import sys
import json
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

from callback_json import ResultCallback
from logger import logger

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
        self.logger = logger
        level = logger.DEBUG
        complete_log = []
        logger.add_consumers(
            (logger.VERBOSE_DEBUG, sys.stdout),
            (level, complete_log.append)
        )
        # after ansible 2.3 need parameter 'sources'
        # create inventory, use path to host config file as source or hosts in a comma separated string
        self.inventory = InventoryManager(loader=self.loader, sources='hosts')
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

    def setSources(self, host_list):
        sources = ""
        if (len(host_list) == 1):
            sources = host_list[0] + ','
        else:
            sources = ','.join(host_list)
        self.inventory = InventoryManager(loader=self.loader, sources=sources)
        self.variable_manager = VariableManager(
            loader=self.loader, inventory=self.inventory)

    def run_planting(self, host_list, task_list):
        play_source = dict(
            name="Planting Play",
            hosts=host_list,
            gather_facts='no',
            tasks=task_list
        )
        play = Play().load(
            play_source, variable_manager=self.variable_manager,
            loader=self.loader)

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


if __name__ == "__main__":
    planting_test = PlantingApi()
    sources = ['10.40.46.64', '10.40.46.62', '10.10.40.220']
    planting_test.setSources(sources)
    hosts = ['10.40.46.64', '10.40.46.62']
    tasks = [
        dict(action=dict(module='command', args='ls')),
        dict(action=dict(module='command', args='df -hl'))
    ]
    planting_test.run_planting(hosts, tasks)
