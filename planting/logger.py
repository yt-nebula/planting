#!/usr/bin/env python
# -*- coding: utf8 -*-
import os
from datetime import date

TIME_ZONE = 'Asia/Shanghai'

LOGGING = {
    'version': 1,
    'disable_existingloggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {module}.{funcName} {lineno:3} {levelname:7} => {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'debug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'logs/ansible_debug_{}.log'.format(date.today().strftime("%Y_%m_%d")),
            'maxBytes': 4194304,  # 4 MB
            'backupCount': 10,
            'level': 'DEBUG',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': 'logs/planting_{}.log'.format(date.today().strftime("%Y_%m_%d")),
            'maxBytes': 4194304,  # 4 MB
            'backupCount': 10,
            'level': 'DEBUG',
        },
        'logstash': {
            'level': 'INFO',
            'class': 'logstash.TCPLogstashHandler',
            'host': 'localhost',
            'port': 5959,
            'version': 1,
            'message_type': 'planting',
            'fqdn': False,
            'tags': ['planting']
        }
    },
    'loggers': {
        'console': {
            'handlers': ['console'],
            'level': os.getenv('PLANTING_LOG_LEVEL', 'INFO')
        },
        'ansible': {
            'handlers': ['debug', 'logstash'],
            'level': os.getenv('ANSIBLE_LOG_LEVEL', 'DEBUG'),
            'propagate': True
        },
        'planting': {
            'handlers': ['file'],
            'level': os.getenv('ANSIBLE_LOG_LEVEL', 'DEBUG'),
        }
    },
}
