#: chain_config
class ChainConfig:
    def __init__(self):
        self.core_asset = 'ECHO'
        self.address_prefix = 'ECHO'
        self.echorand_prefix = 'ECHO'
        self.expire_in_seconds = 15
        self.expire_in_seconds_proposal = 24 * 60 * 60
        self.review_in_seconds_committee = 24 * 60 * 60
        self.networks = None
