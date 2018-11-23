#!/usr/bin/env python3
# encoding: utf-8

import docker

def start_docker():
    client = docker.from_env()

    if client.images.list(name="rastasheep/ubuntu-sshd:16.04") is []:
        client.images.pull("rastasheep/ubuntu-sshd:16.04")

    container = client.containers.run("rastasheep/ubuntu-sshd:16.04", detach=True)

    status = client.containers.get(container.short_id)
    docker_machine = {'ip': status.attrs['NetworkSettings']['IPAddress'], 'username': 'root', 'password': 'root', 'docker_id': container.short_id}
    
    return docker_machine

def kill_docker(docker_id):
    client = docker.from_env()

    container = client.containers.get(docker_id)
    container.stop()
    container.remove()

if __name__ == "__main__":
    docker = start_docker()
    kill_docker(docker.get('docker_id'))