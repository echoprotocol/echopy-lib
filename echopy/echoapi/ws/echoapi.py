class EchoApi:
    def __init__(self, register_query, api_name, params=["", ""]):
        self.register_query = register_query
        self.api_name = api_name
        self.api_id = self.register_query(api_name, params, api=1)

    def rpcexec(self, method, params):
        return self.register_query(method, params, api=self.api_id)
