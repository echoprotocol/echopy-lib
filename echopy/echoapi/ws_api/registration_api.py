# -*- coding: utf-8 -*-
class RegistrationApi:
    def __init__(self, db):
        self.db = db

    def request_registration_task(self):
        return self.db.rpcexec(
            'request_registration_task',
            []
        )

    def submit_registration_solution(self, callback, name, active, echorand_key,
                                     evm_address, nonce, rand_num):
        return self.db.rpcexec(
            'submit_registration_solution',
            [callback, name, active, echorand_key, evm_address, nonce, rand_num]
        )

    def get_registrar(self):
        return self.db.rpcexec(
            'get_registrar',
            []
        )
