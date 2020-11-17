# -*- coding: utf-8 -*-
class RegistrationApi:
    def __init__(self, db):
        self.db = db

    async def request_registration_task(self):
        return await self.db.rpcexec(
            'request_registration_task',
            []
        )

    async def submit_registration_solution(self, callback, name, active, echorand_key,
                                           evm_address, nonce, rand_num):
        return await self.db.rpcexec(
            'submit_registration_solution',
            [callback, name, active, echorand_key, evm_address, nonce, rand_num]
        )

    async def get_registrar(self):
        return await self.db.rpcexec(
            'get_registrar',
            []
        )
