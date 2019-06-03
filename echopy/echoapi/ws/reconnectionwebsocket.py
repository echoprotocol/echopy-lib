# -*- coding: utf-8 -*-
import logging
from collections import Counter
from itertools import cycle
from time import sleep
from .exceptions import RPCError, NumRetriesReached

from .simplewebsocket import SimpleWebsocket
from .echoapi import EchoApi

log = logging.getLogger(__name__)


class ReconnectionWebsocket:
    def __init__(self, user=None, password=None, **kwargs):
        self._connections = dict()
        self._url_counter = Counter()

        self.user = user
        self.password = password
        kwargs.update(dict(user=user, password=password))
        self._kwargs = kwargs

        self.num_retries = kwargs.pop("num_retries", 1)

        self.urls = None
        self._cnt_retries = 0
        self.url = None

        self._active_url = None
        self._active_connection = None

    def _updated_connection(self):
        if self.url[:2] == "ws":
            return SimpleWebsocket(self.url, **self._kwargs)
        else:
            raise ValueError("Only support ws(s) connections!")

    @property
    def connection(self):
        if self._active_url != self.url:
            log.debug(
                "Updating connection from {} to {}".format(self._active_url, self.url)
            )
            self._active_connection = self._updated_connection()
            self._active_url = self.url
        return self._active_connection

    def connect(self, url=None):
        try:
            if self.urls is None and url:
                urls = [url]
                self._url_counter[url] = 0
                self.url = url
                self._active_url = None

                self.urls = cycle(urls)

            self.connection.connect()
        except Exception as e:
            log.warning(str(e))
            self.error_url()
            self.next()
        self.register_apis()


    def disconnect(self):
        if self.urls is not None:
            self.connection.disconnect()
            self._url_counter = Counter()
            self._active_url = None
            self.url = None
            self.urls = None
            self._active_connection = None


    def find_next(self):
        if int(self.num_retries) < 0:
            self._cnt_retries += 1
            sleeptime = (self._cnt_retries - 1) * 2 if self._cnt_retries < 10 else 10
            if sleeptime:
                log.warning(
                    "Lost connection to node during rpcexec(): %s (%d/%d) "
                    % (self.url, self._cnt_retries, self.num_retries)
                    + "Retrying in %d seconds" % sleeptime
                )
                sleep(sleeptime)
            return next(self.urls)

        urls = [
            k
            for k, v in self._url_counter.items()
            if (
                int(self.num_retries) >= 0
                and v <= self.num_retries
                and (k != self.url or len(self._url_counter) == 1)
            )
        ]
        if not len(urls):
            raise NumRetriesReached
        url = urls[0]
        return url

    def reset_counter(self):
        self._cnt_retries = 0
        for i in self._url_counter:
            self._url_counter[i] = 0

    def error_url(self):
        if self.url in self._url_counter:
            self._url_counter[self.url] += 1
        else:
            self._url_counter[self.url] = 1

    def next(self):
        self.connection.disconnect()
        self.url = self.find_next()
        self.connect()

    def post_process_exception(self, exception):
        raise exception


    def register_apis(self):
        """ This method is called right after connection and has previously
            been used to register to different APIs within the backend that are
            considered default. The requirement to register to APIs has been
            removed in some systems.
        """
        self._database = EchoApi(self.make_query, 'database')
        self._network_broadcast = EchoApi(self.make_query, 'network_broadcast')
        self._history = EchoApi(self.make_query, 'history')
        self._registration = EchoApi(self.make_query, 'registration')
        self._asset = EchoApi(self.make_query, 'asset')

        self._login = EchoApi(self.make_query, 'login')
        self._login.api_id = 1
        self._network_node = EchoApi(self.make_query, 'network_node')

    def make_query(self, name, params, *args, **kwargs):
        while True:
            try:
                func = self.connection.__getattr__(name)
                r = func(params, *args, **kwargs)
                self.reset_counter()
                break
            except KeyboardInterrupt:
                raise
            except RPCError as e:
                """ When the backend actual returns an error
                """
                self.post_process_exception(e)
                break
            except IOError:
                import traceback

                log.debug(traceback.format_exc())
                log.warning("Connection was closed remotely.")
                log.warning("Reconnecting ...")
                self.error_url()
                self.next()
            except Exception as e:
                import traceback

                log.debug(traceback.format_exc())
                self.error_url()
                self.next()

        return r
