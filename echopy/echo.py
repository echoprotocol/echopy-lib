from .echoapi import Api
from .transaction import Transaction
from .echobase.config import Config
from .echobase.utils import solve_registration_task
from .echobase.account import BrainKey


class Echo:

    def __init__(self):
        self.api = Api()
        self.config = Config()
        self.brain_key = BrainKey

    def solve_registration_task(self, block_id, rand_num, difficulty):
        return solve_registration_task(block_id, rand_num, difficulty)

    def register_account(self, callback, name, active, echorand, evm_address=None):
        if self.api.ws.connection is None:
            raise AttributeError("Connection is needed: use 'connect' method for connecting to node")
        task = self.api.registration.request_registration_task()
        nonce = self.solve_registration_task(
            task["block_id"],
            task["rand_num"],
            task["difficulty"]
        )
        return self.api.registration.submit_registration_solution(
            callback,
            name,
            active,
            echorand,
            evm_address,
            nonce,
            task["rand_num"]
        )

    def create_transaction(self):
        return Transaction(self.api)

    def connect(self, url, debug=False):
        self.api.connect(url, debug)

    def disconnect(self):
        self.api.disconnect()
