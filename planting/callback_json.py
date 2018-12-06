#!/usr/bin/env python
# -*- coding: utf8 -*-

import copy
import os
import json
import datetime
import time
from collections import defaultdict

from ansible.plugins.callback import CallbackBase
from ansible.playbook.play import Play
from ansible.vars.clean import strip_internal_keys

from planting.logger import Logger


def current_time():
    return '%sZ' % datetime.datetime.utcnow().isoformat()


class ResultCallback(CallbackBase):
    def __init__(self, display=None):
        super(ResultCallback, self).__init__(display)
        self.results = []
        self.output = []
        self.playbook = {}
        self._logger = Logger()
        self.host_ok = defaultdict(list)
        self.host_unreachable = defaultdict(list)
        self.host_failed = defaultdict(list)
        self.success = True
        level = self._logger.DEBUG
        complete_log = []
        # from log config
        self.output_path = 'ansible_debug_{time}.log'.format(
            time=time.strftime(
                '%Y_%m_%d', time.localtime(
                    time.time())))

        f = open(self.output_path, 'a+')
        self._playbook_name = None
        self._logger.add_consumers(
            (self._logger.VERBOSE_DEBUG, f), (level, complete_log.append))

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
        self._playbook_name = os.path.splitext(playbook._file_name)[0]

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
        self._logger.debug(json.dumps({host.name: self.results[-1]}, indent=4))
        self.host_ok[result._host.get_name()].append(clean_result)

    def v2_playbook_on_stats(self, stats):
        """Display info about playbook statistics"""
        hosts = sorted(stats.processed.keys())

        summary = {}
        for h in hosts:
            s = stats.summarize(h)
            summary[h] = s

        self.playbook['plays'] = self.results
        self.playbook['stats'] = summary
        self.output.append(self.playbook)

        json.dump(self.output, open(self.output_path, 'w'),
                  indent=4, sort_keys=True, separators=(',', ': '))

    def v2_runner_on_failed(self, result, **kwargs):
        host = result._host
        myresult = copy.deepcopy(result._result)
        clean_result = strip_internal_keys(myresult)
        self.results[-1]['tasks'][-1]['hosts'][host.name] = clean_result
        end_time = current_time()
        self.results[-1]['tasks'][-1]['task']['duration']['end'] = end_time
        self.results[-1]['play']['duration']['end'] = end_time
        self._logger.error(json.dumps({host.name: self.results[-1]}, indent=4))
        self.host_failed[result._host.get_name()].append(clean_result)
        self.success = False

    def v2_runner_on_unreachable(self, result, **kwargs):
        host = result._host
        myresult = copy.deepcopy(result._result)
        clean_result = strip_internal_keys(myresult)
        self.results[-1]['tasks'][-1]['hosts'][host.name] = clean_result
        end_time = current_time()
        self.results[-1]['tasks'][-1]['task']['duration']['end'] = end_time
        self.results[-1]['play']['duration']['end'] = end_time
        self._logger.error(json.dumps({host.name: self.results[-1]}, indent=4))
        self.host_unreachable[result._host.get_name()].append(clean_result)
        self.success = False

    v2_runner_on_skipped = v2_runner_on_ok
