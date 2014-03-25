#!/usr/bin/env python

"""
This file defines the configuration settings for the simulator;
change them according to your environment, or use a local_settings.py
file which is excluded from source control.

"""

DATA_FOLDER   = '/tmp'
ACCOUNTS_LIST = 'accounts.txt'

try:
    from local_settings import *
except ImportError:
    pass
