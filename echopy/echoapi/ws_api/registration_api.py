# -*- coding: utf-8 -*-
class RegistrationApi:
    def __init__(self, db):
        self.db = db

    async def register_account(self, name, owner_key, active_key, memo_key, echorand_key):
        return await self.db.rpcexec('register_account', [name, owner_key, active_key, memo_key, echorand_key])
