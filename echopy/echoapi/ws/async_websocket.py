# -*- coding: utf-8 -*-
import ssl
import json
import logging
from async_promises import Promise
import asyncio
import websockets
from websockets import ConnectionClosed
from .exceptions import RPCError, NumRetriesReached
from .echoapi import EchoApi, register_echo_api

log = logging.getLogger(__name__)


class AsyncWebsocket:
    def __init__(self, *args, **kwargs):
        self.promises = {}
        self._request_id = 0
        self.num_retries = kwargs.get("num_retries", 1)
        self.url = None
        self._listen_future = None
        self._loop = None
        self.ws = None

    def get_request_id(self, increment=True):
        if increment:
            self.increment_request_id()
        return self._request_id

    def increment_request_id(self):
        self._request_id += 1

    async def listen(self):
        while True:
            res = json.loads(await self.ws.recv())
            self.promises[res['id']](res)

    async def connect(self, url):
        self.url = url
        log.debug("Trying to connect to node %s" % self.url)
        self._request_id = 0
        self._loop = asyncio.get_event_loop()
        if self.url[:3] == "wss":
            self.ws = await websockets.connect(self.url, ssl=True)
        else:
            self.ws = await websockets.connect(self.url)
        self._listen_future = asyncio.ensure_future(self.listen(), loop=self._loop)
        await self.register_apis()

    async def disconnect(self):
        if self.ws:
            try:
                self._listen_future.cancel()
                self._listen_future = None
                await self.ws.close()
                self.ws = None
                self._loop = None

            except Exception as e:
                raise(e)

    def _save_promise(self, resolve, reject):
        self.promises[self.get_request_id()] = resolve

    def parse_response(self, res):
        if "error" in res:
            if "detail" in res["error"]:
                raise RPCError(res["error"]["detail"])
            else:
                raise RPCError(res["error"]["message"])
        else:
            return res['result']


    async def make_query(self, name, params, *args, **kwargs):
        if self.url:
            if not self.ws:
                await self.connect(self.url)
        else:
            raise(Exception('Socket is not connected'))

        api_id = 0 if 'api' not in kwargs else kwargs['api']

        promise = Promise(self._save_promise)

        payload = {
            'method': 'call',
            'params': [api_id, name, params],
            'jsonrpc': '2.0',
            'id': self.get_request_id(increment=False)
        }
        while True:
            try:
                await self.ws.send(json.dumps(payload, ensure_ascii=False).encode("utf8"))

                res = await promise

                res = self.parse_response(res)

                break

            except ConnectionClosed:
                await self.connect(self.url)

        return res

    async def register_apis(self):
        """ This method is called right after connection and has previously
            been used to register to different APIs within the backend that are
            considered default. The requirement to register to APIs has been
            removed in some systems.
        """
        apis = ['database', 'network_broadcast', 'history', 'registration', 'asset', 'login', 'network_node']
        self._database, self._network_broadcast, self._history, self._registration, self._asset, self._login,\
            self._network_node = await Promise.all([register_echo_api(self, api_unit) for api_unit in apis])
        self._login.api_id = 1
