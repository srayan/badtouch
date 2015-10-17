# -*- coding: utf-8 -*-

import logging

from cached_property import cached_property_with_ttl

from .http import BadTouchHttp
from .key import Key


log = logging.getLogger(__name__)


class BadTouch(object):
    def __init__(self, device, http=BadTouchHttp):
        self._device = device
        self._http = http(base_url="http://{}:8090".format(self._device))
        self.key = Key(self)

    @cached_property_with_ttl(ttl=5 * 60)
    def info(self):
        return self._http.get("/info")["info"]

    @property
    def now_playing(self):
        return self._http.get("/now_playing")["nowPlaying"]

    @cached_property_with_ttl(ttl=60)
    def presets(self):
        return self._http.get("/presets")["presets"]["preset"]

    def select_key(self, key):
        return self.key.send_key(key)
