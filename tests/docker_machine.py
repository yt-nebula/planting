#!/usr/bin/env python3
# -*- coding: utf8 -*-

import docker


class Container(object):
    def __init__(self, **kwargs):
        self.ip = kwargs['ip']
        self.username = kwargs['username']
        self.password = kwargs['password']
        self.container_id = kwargs['container_id']


def start_image():
    client = docker.from_env()
    if client.images.list(name="blueduc/planting-test") is []:
        client.images.pull("blueduc/planting-test")


def start_container():
    client = docker.from_env()
    container = client.containers.run("blueduc/planting-test", detach=True)
    status = client.containers.get(container.short_id)
    docker_machine = Container(
        ip=status.attrs['NetworkSettings']['IPAddress'],
        username="root",
        password="root",
        container_id=container.short_id)
    return docker_machine


def kill_container(container_id):
    client = docker.from_env()
    container = client.containers.get(container_id)
    container.stop()
    container.remove()
