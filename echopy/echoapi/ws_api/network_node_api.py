# -*- coding: utf-8 -*-
class NetworkNodeApi:
    def __init__(self, db):
        self.db = db

    def set_consensus_message_callback(self, callback):
        return self.db.rpcexec('set_consensus_message_callback', [callback])
