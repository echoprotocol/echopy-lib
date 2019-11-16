# -*- coding: utf-8 -*-

from .ws import WS
from .ws_api.asset_api import AssetApi
from .ws_api.login_api import LoginApi
from .ws_api.network_api import NetworkApi
from .ws_api.database_api import DatabaseApi
from .ws_api.history_api import HistoryApi
from .ws_api.registration_api import RegistrationApi


class Api:
    def __init__(self):
        self.ws = WS()

    def connect(self, url, debug):
        self.ws.connect(url, debug)
        self.database = DatabaseApi(self.ws.db_api)
        self.asset = AssetApi(self.ws.asset_api)
        self.network = NetworkApi(self.ws.network_api)
        self.history = HistoryApi(self.ws.history_api)
        self.registration = RegistrationApi(self.ws.registration_api)
        self.login = LoginApi(self.ws.login_api)

    def disconnect(self):
        self.ws.disconnect()

__all__ = [
    "ws",
    "ws_api"
]
