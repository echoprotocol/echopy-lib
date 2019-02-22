class AssetApi:
    def __init__(self, db):
        self.db = db

    def get_asset_holders(self, asset_id, start, limit):
        return self.db.rpcexec('get_asset_holders', [asset_id, start, limit])

    def get_asset_holders_count(self, asset_id):
        return self.db.rpcexec('get_asset_holders_count', [asset_id])

    def get_all_asset_holders(self):
        return self.db.rpcexec('get_all_asset_holders', [])
