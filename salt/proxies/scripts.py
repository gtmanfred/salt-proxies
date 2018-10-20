# -*- coding -*-
'''
Entry point for salt-proxies
'''
# Import Salt Libraries
import salt.proxies.client


def salt_proxies_main():
    salt.proxies.client.SaltProxies().run()
