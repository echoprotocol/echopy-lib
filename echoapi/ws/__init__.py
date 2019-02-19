# -*- coding: utf-8 -*-

from .reconnectionwebsocket import ReconnectionWebsocket

# import validate
# import constants


class WS(ReconnectionWebsocket):
    def __init__(self, urls, user=None, password=None, **kwargs):
        super().__init__(urls, user, password, **kwargs)

    @property
    def db_api(self):
        return self._database

    @property
    def network_api(self):
        return self._network_broadcast

    @property
    def history_api(self):
        return self._history

    @property
    def registration_api(self):
        return self._registration

    @property
    def asset_api(self):
        return self._asset

    @property
    def login_api(self):
        return self._login

    @property
    def network_node_api(self):
        return self._network_node
