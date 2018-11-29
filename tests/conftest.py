#!/usr/bin/env python3
# encoding: utf-8
import os
import time
import re

import pytest
import docker


from tests.docker_machine import start_image, kill_container, start_container
from planting.machine import Machine


@pytest.fixture(scope="session")
def image_initialization(request):
    start_image()
    os.environ['ANSIBLE_HOST_KEY_CHECKING'] = 'False'

@pytest.fixture(scope="function")
def machine(image_initialization):
    container = start_container()
    os.system("ssh-keygen -R " + container.ip)
    retries = 20
    for _ in range(retries):
        output = os.popen("docker top " + container.container_id).read()
        pattern = re.compile(r'sshd')
        if len(pattern.findall(output)) is 2:
            break
        time.sleep(1)
    machine = Machine(
        ip=container.ip,
        remote_user=container.username,
        password=container.password,
        python='/root/venv/bin/python')
    machine.register_all()
    yield machine
    # kill_container(container.container_id)
