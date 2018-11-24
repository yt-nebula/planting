#!/usr/bin/env python
# encoding: utf-8
import json
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.inventory.host import Host
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

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result


class Machine(object):
    def __init__(self, ip, username=None, password=None, port='22'):
        self.ops = Options(connection='ssh',
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
        self.inventory = InventoryManager(loader=self.loader)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
        host_info = Host(name=ip, port=port)
        self.variable_manager.set_host_variable(host_info, 'ansible_user', username)
        self.variable_manager.set_host_variable(host_info, 'ansible_pass', password)
        self.host_pattern = ip

    class Network(object):
        @staticmethod
        def port(port):
            return

        @staticmethod
        def process(process):
            return

    class File(object):
        @staticmethod
        def copy(path, dest):
            return

    def run_ansible(self, task_list):
        """use ansible module

        Args:
            task_list: ansible module and args
        Returns:
            json: result return

        """
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
            tqm._stdout_callback = self.results_callback
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

        results_raw = dict()
        results_raw['success'] = dict()
        results_raw['failed'] = dict()
        results_raw['unreachable'] = dict()

        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = json.dumps(result._result)

        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result['msg']

        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result['msg']

        print(results_raw)


if __name__ == "__main__":
    node1 = Machine(ip='127.0.0.1', username="aaa", password="1234567", port='22')
    tasks = [
        dict(action=dict(module='command', args='ls'))
    ]
    node1.run_ansible(tasks)
    node1.Network.port(port=['22'])
    node1.Network.process(process=['java', 'tomcat'])
    node1.File.copy(path='path', dest='dest')
