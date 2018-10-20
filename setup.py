#!/usr/bin/env python
'''
A CLI front-end to a running salt-proxies system
'''
import json
import os
import re
import sys

from distutils.core import setup
from distutils.command import sdist, install_data

setup_kwargs = {
    'name': 'salt-proxies',
    'description': __doc__.strip(),
    'author': 'Daniel Wallace',
    'author_email': 'daniel@gtmanfred.com',
    'url': 'http://saltstack.com',
    'classifiers': [
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Networking',
    ],
    'packages': [
        'salt.proxies',
    ],
    'package_data': {
        'salt.proxies': ['version.json'],
    },
    'entry_points': {
        'console_scripts': [
            'salt-proxies = salt.proxies.scripts:salt_proxies_main',
        ],
    },
}


def read_version_tag():
    git_dir = os.path.join(os.path.dirname(__file__), '.git')

    if os.path.isdir(git_dir):
        import subprocess

        try:
            p = subprocess.Popen(['git', 'describe'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
        except Exception:
            pass
        else:
            return out.strip() or None

    else:
        return read_version_from_json_file()

    return None


def read_version_from_json_file():
    with open(os.path.join(os.path.dirname(__file__), 'salt', 'proxies', 'version.json')) as f:
        return json.load(f)['version']


def parse_version_tag(tag):
    '''
    Parse the output from Git describe

    Returns a tuple of the version number, number of commits (if any), and the
    Git SHA (if available).
    '''
    if isinstance(tag, bytes):
        tag = tag.decode()
    if not tag or '-g' not in tag:
        return tag, None, None

    match = re.search('(?P<version>.*)-(?P<num_commits>[0-9]+)-g(?P<sha>[0-9a-fA-F]+)', tag)

    if not match:
        return tag, None, None

    match_dict = match.groupdict()
    return (
        match_dict.get('version'),
        match_dict.get('num_commits'),
        match_dict.get('sha'))


def get_version():
    '''
    Return a tuple of the version and Git SHA
    '''
    version, num_commits, sha = parse_version_tag(read_version_tag())
    if sha:
        version = '{0}.dev{1}'.format(version, num_commits)
    return version, sha


def write_version_file(base_dir):
    ver_path = os.path.join(base_dir, 'salt', 'proxies', 'version.json')
    version, sha = get_version()

    with open(ver_path, 'wb' if sys.version_info[0] == 2 else 'w') as f:
        json.dump({'version': version, 'sha': sha}, f)


class SaltProxiesSdist(sdist.sdist):
    '''
    Write the version.json file to the sdist tarball build directory
    '''
    def make_release_tree(self, base_dir, files):
        sdist.sdist.make_release_tree(self, base_dir, files)
        write_version_file(base_dir)


class SaltProxiesInstallData(install_data.install_data):
    '''
    Write the version.json file to the installation directory
    '''
    def run(self):
        install_cmd = self.get_finalized_command('install')
        install_dir = getattr(install_cmd, 'install_lib')
        write_version_file(install_dir)

        return install_data.install_data.run(self)


if __name__ == '__main__':
    version, sha = get_version()

    setup(cmdclass={
        'sdist': SaltProxiesSdist,
        'install_data': SaltProxiesInstallData,
    }, version=version, git_sha=sha, **setup_kwargs)
