# -*- coding: utf-8 -*-
class NetworkNodeApi:
    def __init__(self, db):
        self.db = db

    async def set_consensus_message_callback(self, callback):
        return await self.db.rpcexec('set_consensus_message_callback', [callback])
