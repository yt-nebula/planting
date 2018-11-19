#!/usr/bin/env python
# encoding: utf-8

import json
from planting import Planting

if __name__ == "__main__":
    # ********
    node_list_1 = ['10.40.40.183','10.40.50.132']
    opreation = Planting(
        machine=node_list_1,
        module_name='get_url',
        url='http://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/MLbook2016-HowToUse.pdf',
        dest='~/MLbook2016-HowToUse.pdf',
    ).run()

    # ********
    node_list_2 = ['10.40.40.180']
    opreation = Planting(
        machine=node_list_2,
        module_name='command',
        url='~/book.tar.gz',
        dest='~',
    ).run()