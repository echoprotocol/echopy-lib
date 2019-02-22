#: ws_constants
class WSConfig:
    def __init__(self):
        self.connection_timeout = 5 * 1000
        self.max_retries = 0
        self.ping_timeout = 13 * 1000
        self.ping_interval = 20 * 1000
        self.debug = False
