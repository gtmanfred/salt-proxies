# -*- coding: utf-8 -*-
'''
SaltProxies Client
'''
# Import Python Libraries
import multiprocessing
import os
import yaml

# Import Salt Libraries
import salt.client
import salt.config
import salt.utils.args


class SaltProxies(object):

    processes = []

    def __init__(self, opts):
        self.options = opts
        self.args, self.kwargs = salt.utils.args.parse_input(opts.get('args', []), condition=False)
        cfile = opts.get('config', './config/config.yml')
        if os.path.isfile(cfile):
            with open(cfile, 'r') as configfile:
                self.config = yaml.safe_load(configfile)
        else:
            self.config = {}
        self.opts = salt.config.proxy_config(path=opts.get('proxy_config', './config/proxy.yml'))
        self.opts['file_client'] = 'local'
        self.opts['file_roots'] = {'base': [opts.get('states', './states/')]}
        self.opts['pillar_roots'] = {'base': [opts.get('pillars', './pillars/')]}
        self.opts['cachedir'] = f'{os.getcwd()}/.cache/'

    @property
    def output(self):
        module = salt.loader.minion_mods(self.opts, whitelist=[self.options['fun'].split('.')[0]])
        try:
            oput = module[self.options['fun']].__outputter__
        except (KeyError, AttributeError, TypeError):
            oput = 'nested'
        return oput

    def __call__(self, proxyid):
        opts = self.opts.copy()
        opts['id'] = proxyid
        client = salt.client.ProxyCaller(mopts=opts)
        if not client.cmd(f'match.{self.options["match"]}', tgt=self.options['target']):
            return
        ret = client.cmd(self.options['fun'], *self.args, **self.kwargs)
        salt.output.display_output(
            {proxyid: ret},
            self.options['output'] or self.output,
            opts=self.opts
        )

    def run(self):
        with multiprocessing.Pool(self.options['procs']) as pool:
            pool.map(self, self.config.get('proxies', []))
