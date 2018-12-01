#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
os.sys.path.append('/Users/panjianlong/github/planting/')


from machine import Machine
from planting.planting_module import operations

if __name__ == '__main__':
    node = Machine('10.40.50.132', 'linuxadmin', 'Hello=111!', python='/usr/bin/python')
    node.register_all()
    node.list_all_module()
    # node.create(path="~/dir", state="dir")
    # node.create(path="~/dir/1.txt", state="file")
    # node.jsoninfile(
    #     path="~/test.conf", 
    #     keys=["cluster", "list", 0], 
    #     val={"ee": 22})

