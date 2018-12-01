#!/usr/bin/env python
# -*- coding: utf8 -*-

from machine import Machine
from planting.planting_module import operations

if __name__ == '__main__':
    node = Machine('xxx.xxx.xxx.xxx', 'xxxx', 'xxxx')
    node.register_all()
    node.list_all_module()
    node.create(path="~/dir", state="dir")
    node.create(path="~/dir/1.txt", state="file")
    node.jsoninfile(path="~/cluster_config.json", keys=["machine_list", 0, "resource_capacity"], val="xxxx")
    node.jsoninfile(path="~/cluster_config.json", keys=["machine_list", 1], val="xxxx")
    #  node.create(path="~/dir", state="dir")
    # node.create(path="~/dir/1.txt", state="file")
    #
