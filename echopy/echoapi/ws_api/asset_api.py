class AssetApi:
    def __init__(self, db):
        self.db = db

    async def get_asset_holders(self, asset_id, start, limit):
        return await self.db.rpcexec(
            'get_asset_holders',
            [asset_id, start, limit]
        )

    async def get_asset_holders_count(self, asset_id):
        return await self.db.rpcexec(
            'get_asset_holders_count',
            [asset_id]
        )

    async def get_all_asset_holders(self):
        return await self.db.rpcexec(
            'get_all_asset_holders',
            []
        )
