#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from importlib.metadata import version
from typing import Dict, Optional
from urllib.parse import urljoin, urlparse

import requests


class PyProject():

    def __init__(self, root_url: str, useragent: Optional[str]=None,
                 *, proxies: Optional[Dict[str, str]]=None):
        '''Query a specific instance.

        :param root_url: URL of the instance to query.
        :param useragent: The User Agent used by requests to run the HTTP requests against the instance.
        :param proxies: The proxies to use to connect to theinstance - More details: https://requests.readthedocs.io/en/latest/user/advanced/#proxies
        '''
        self.root_url = root_url

        if not urlparse(self.root_url).scheme:
            self.root_url = 'http://' + self.root_url
        if not self.root_url.endswith('/'):
            self.root_url += '/'
        self.session = requests.session()
        self.session.headers['user-agent'] = useragent if useragent else f'PyProject / {version("pyproject")}'
        if proxies:
            self.session.proxies.update(proxies)

    @property
    def is_up(self) -> bool:
        '''Test if the given instance is accessible'''
        try:
            r = self.session.head(self.root_url)
        except requests.exceptions.ConnectionError:
            return False
        return r.status_code == 200

    def redis_up(self) -> Dict:
        '''Check if redis is up and running'''
        r = self.session.get(urljoin(self.root_url, 'redis_up'))
        return r.json()
