#!/usr/bin/env python
# encoding: utf-8

from machine import Machine
from planting_module import operations

if __name__ == '__main__':
    node = Machine('10.40.50.132', 'linuxadmin', 'Hello=111!')
    node.register_all()
    node.list_all_module()
    # node.create(path="~/dir", state="dir")
    # node.create(path="~/dir/1.txt", state="file")

    # node.fetch(src='~/cluster_config.json', dest='./')
    # node.template(src='./10.40.50.132/home/linuxadmin/cluster_config.json', dest='~/cluster_config.json')
    node.jsoninfile(path="~/cluster_config.json", keys=["machine_list", 1], val="xxxx")