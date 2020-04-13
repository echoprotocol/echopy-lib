class DidApi:
    def __init__(self, db):
        self.db = db

    def get_did_object(self, did_object_id):
        return self.db.rpcexec(
            'get_did_object',
            [did_object_id]
        )

    def get_key_by_id_string(self, key_id):
        return self.db.rpcexec(
            'get_key_by_id_string',
            [key_id]
        )

    def get_keys_by_id_string(self, did_id):
        return self.db.rpcexec(
            'get_keys_by_id_string',
            [did_id]
        )
