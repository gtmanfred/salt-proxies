# -*- coding: utf-8 -*-
'''
SaltProxies Client
'''
# Import Python Libraries
import multiprocessing

# Import Salt Libraries
import salt.config

# Import SaltProxies Libraries
import salt.proxies.parser


class SaltProxies(object):

    def __init__(self):
        self.options = salt.proxies.parser.parse_args()

    def run(self):
        pass
