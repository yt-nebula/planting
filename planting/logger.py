#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import time

rt = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
log_path = os.path.dirname(os.getcwd()) + '/logs/'
logfile = rt + log_path + '.log'
