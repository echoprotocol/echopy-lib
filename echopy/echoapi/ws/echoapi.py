class EchoApi:
    def __init__(self, ws, api_name, api_id):
        self.api_name = api_name
        self.api_id = api_id
        self._ws = ws

    async def rpcexec(self, method, params):
        res = await self._ws.make_query(method, params, api=self.api_id)
        return res


async def register_echo_api(ws, api_name):
    api_id = await ws.make_query(api_name, ["", ""] if api_name == 'login' else [], api=1)
    return EchoApi(ws, api_name, api_id)
