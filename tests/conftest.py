#!/usr/bin/env python3
# encoding: utf-8

import pytest
from tests.docker_machine import start_docker, kill_docker

@pytest.fixture(scope="session")
def dokcer_machine(self, request):
    self.docker = start_docker()

    def fin():
        kill_docker(self.docker.docker_id)

    request.addfinalizer(fin)
