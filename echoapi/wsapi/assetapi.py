# -*- coding: utf-8 -*-
class AssetApi:
    def __init__(self, connection):
        self.connection = connection

    def get_asset_holders(self, asset_id, start, limit):
        return self.connection.rpcexec('get_asset_holders', [asset_id, start, limit])

    def get_asset_holders_count(self, asset_id):
        return self.connection.rpcexec('get_asset_holders_count', [asset_id])

    def get_all_asset_holders(self):
        return self.connection.rpcexec('get_all_asset_holders', [])
