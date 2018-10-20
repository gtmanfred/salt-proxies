# -*- coding -*-
'''
Entry point for salt-proxies
'''
# Import Python Libraries
import click

# Import Salt Libraries
import salt.proxies.client


@click.command()
@click.option('--config', default='./config/config.yml', help='salt-proxies config file')
@click.option('--proxy-config', default='./config/proxy.yml', help='proxy minion config file')
@click.option('--states', default='./states/', help='directory with states')
@click.option('--pillars', default='./pillars/', help='directory with pillars')
@click.option('--procs', default=1, help='number of processes to use')
@click.option('--output', default=None, help='outputter to use')
@click.option('--match', default='compound', help='matcher to use for proxy minions')
@click.argument('target', nargs=1)
@click.argument('fun', nargs=1)
@click.argument('args', nargs=-1)
def salt_proxies_main(**kwargs):
    salt.proxies.client.SaltProxies(opts=kwargs).run()
