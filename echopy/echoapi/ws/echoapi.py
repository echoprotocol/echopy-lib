class EchoApi:
    def __init__(self, register_query, api_name):
        self.register_query = register_query
        self.api_name = api_name
        self.api_id = self.register_query(api_name, ["", ""] if self.api_name == 'login' else [], api=1)

    def rpcexec(self, method, params):
        return self.register_query(method, params, api=self.api_id)
