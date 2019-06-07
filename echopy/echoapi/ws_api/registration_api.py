# -*- coding: utf-8 -*-
class RegistrationApi:
    def __init__(self, db):
        self.db = db

    def register_account(self, callback, name, active_key, echorand_key):
        return self.db.rpcexec('register_account', [callback, name, active_key, echorand_key])
