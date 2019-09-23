# -*- coding: utf-8 -*-
class RegistrationApi:
    def __init__(self, db):
        self.db = db

    def register_account(self, callback, name, active_key, echorand_key):
        return self.db.rpcexec('register_account', [callback, name, active_key, echorand_key])

    def request_registration_task(self):
        return self.db.rpcexec('request_registration_task', [])

    def submit_registration_solution(self, callback, name, active, echorand_key, nonce, rand_num):
        return self.db.rpcexec(
            'submit_registration_solution',
            [callback, name, active, echorand_key, nonce, rand_num]
        )
