#!/usr/bin/env python
# -*- coding: utf8 -*-

import copy
import datetime
import json
import logging
import os
import socket
from collections import defaultdict

from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.clean import strip_internal_keys


def current_time():
    return '%sZ' % datetime.datetime.utcnow().isoformat()


class ResultCallback(CallbackBase):
    def __init__(self, display=None):
        super(ResultCallback, self).__init__(display)
        self.results = []
        self.output = []
        self.playbook = {}
        self.logger = logging.getLogger('ansible')
        self.host_ok = defaultdict(list)
        self.host_unreachable = defaultdict(list)
        self.host_failed = defaultdict(list)
        self.success = True
        self.finished = False
        self.errors = 0
        self._playbook_name = None
        self.hostname = socket.gethostname()
        self.start_time = None

    def play_info(self):
        return self.results[-1]["play"]

    def task_list(self):
        return self.results[-1]["tasks"]

    def _new_playbook(self, play: Play):
        hostvars = next(iter(play._variable_manager._hostvars.values()))
        self._playbook_name = None

        playbook = hostvars.get('playbook')
        self.playbook['playbook'] = playbook

    def _new_play(self, play):
        return {
            'play': {
                'name': play.name,
                'id': str(play._uuid),
                'duration': {
                    'start': current_time()
                }
            },
            'tasks': []
        }

    def _new_task(self, task):
        data = {
            'task': {
                'name': task.name,
                'id': str(task._uuid),
                'duration': {
                    'start': current_time()
                }
            },
            'hosts': {}
        }
        if task._role:
            data['role'] = {
                'name': task._role.get_name(),
                'id': str(task._role._uuid),
                'path': task._role._role_path,
            }
        return data

    def v2_playbook_on_start(self, playbook):
        self.finished = False
        self._playbook_name = os.path.splitext(playbook._file_name)[0]
        data = {
            'status': "OK",
            'host': self.hostname,
            'ansible_type': "start",
            'ansible_playbook': self.playbook,
        }
        self.logger.info("ansible start", extra=data)

    def v2_playbook_on_play_start(self, play):
        if self._playbook_name:
            self._new_playbook(play)

        self.results.append(self._new_play(play))

    def v2_playbook_on_task_start(self, task, is_conditional):
        self.results[-1]['tasks'].append(self._new_task(task))

    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        myresult = copy.deepcopy(result._result)
        clean_result = strip_internal_keys(myresult)
        self.results[-1]['tasks'][-1]['hosts'][host.name] = clean_result
        end_time = current_time()
        self.results[-1]['tasks'][-1]['task']['duration']['end'] = end_time
        self.results[-1]['play']['duration']['end'] = end_time
        self.host_ok[result._host.get_name()].append(clean_result)
        self.logger.debug(json.dumps({host.name: self.results[-1]}, indent=4))
        data = {
            'status': "OK",
            'host': self.hostname,
            'ansible_type': "task",
            'ansible_playbook': self.playbook,
            'ansible_host': result._host.name,
            'ansible_task': result._task,
            'ansible_result': self._dump_results(result._result)
        }
        self.success = True
        self.finished = True
        self.logger.info("ansible ok", extra=data)

    def play_status(self):
        return self.finished

    def v2_playbook_on_stats(self, stats):
        end_time = datetime.utcnow()
        runtime = end_time - self.start_time
        summarize_stat = {}
        for host in stats.processed.keys():
            summarize_stat[host] = stats.summarize(host)
        if self.errors == 0:
            status = "OK"
            self.success = True
        else:
            status = "FAILED"
            self.success = False
        self.finished = True
        data = {
            'status': status,
            'host': self.hostname,
            'ansible_type': "finish",
            'ansible_playbook': self.playbook,
            'ansible_playbook_duration': runtime.total_seconds(),
            'ansible_result': json.dumps(summarize_stat),
        }
        self.logger.info("ansible stats", extra=data)

    def v2_runner_on_failed(self, result, **kwargs):
        host = result._host
        myresult = copy.deepcopy(result._result)
        clean_result = strip_internal_keys(myresult)
        self.results[-1]['tasks'][-1]['hosts'][host.name] = clean_result
        end_time = current_time()
        self.results[-1]['tasks'][-1]['task']['duration']['end'] = end_time
        self.results[-1]['play']['duration']['end'] = end_time
        self.logger.error(json.dumps({host.name: self.results[-1]}, indent=4))
        self.host_failed[result._host.get_name()].append(clean_result)
        data = {
            'status': "FAILED",
            'host': self.hostname,
            'ansible_type': "task",
            'ansible_playbook': self.playbook,
            'ansible_host': result._host.name,
            'ansible_task': result._task,
            'ansible_result': self._dump_results(result._result)
        }
        self.errors += 1
        self.success = False
        self.finished = True
        self.logger.error("ansible failed", extra=data)

    def v2_runner_on_unreachable(self, result, **kwargs):
        host = result._host
        myresult = copy.deepcopy(result._result)
        clean_result = strip_internal_keys(myresult)
        self.results[-1]['tasks'][-1]['hosts'][host.name] = clean_result
        end_time = current_time()
        self.results[-1]['tasks'][-1]['task']['duration']['end'] = end_time
        self.results[-1]['play']['duration']['end'] = end_time
        self.logger.error(json.dumps({host.name: self.results[-1]}, indent=4))
        self.host_unreachable[result._host.get_name()].append(clean_result)
        data = {
            'status': "UNREACHABLE",
            'host': self.hostname,
            'ansible_type': "task",
            'ansible_playbook': self.playbook,
            'ansible_host': result._host.name,
            'ansible_task': result._task,
            'ansible_result': self._dump_results(result._result)
        }
        self.errors += 1
        self.success = False
        self.finished = True
        self.logger.error("ansible unreachable", extra=data)      

    v2_runner_on_skipped = v2_runner_on_ok
