import unittest
from .fixtures import (connect_echo, broadcast_operation, disconnect_echo,
                       get_random_asset_symbol, _from, _to, get_keys, random_string)
from echopy.echoapi.ws.exceptions import RPCError
from copy import deepcopy
from .subtests import subtest_call_contract, subtest_asset_issue

class OperationsTest(unittest.TestCase):
    def setUp(self):
        self.echo = connect_echo()

    def tearDown(self):
        disconnect_echo(self.echo)

    def test_transfer_with_full_fee(self):
        transfer_props = {
            'fee': {
                'asset_id': '1.3.0',
                'amount': 20
            },
            'from': _from,
            'to': _to,
            'amount': {
                'asset_id': '1.3.0',
                'amount': 1
            }
        }

        transfer_broadcast_result = broadcast_operation(
            echo=self.echo,
            operation_ids=self.echo.config.operation_ids.TRANSFER,
            props=transfer_props
        )

        self.assertNotIn('error', transfer_broadcast_result)

    def test_transfer_without_asset_id(self):
        transfer_props = {
            'fee': {
                'amount': 30
            },
            'from': _from,
            'to': _to,
            'amount': {
                'asset_id': '1.3.0',
                'amount': 1
            }
        }

        transfer_broadcast_result = broadcast_operation(
            echo=self.echo,
            operation_ids=self.echo.config.operation_ids.TRANSFER,
            props=transfer_props
        )

        self.assertNotIn('error', transfer_broadcast_result)

    def test_transfer_without_amount(self):
        transfer_props = {
            'fee': {
                'asset_id': '1.3.0'
            },
            'from': _from,
            'to': _to,
            'amount': {
                'asset_id': '1.3.0',
                'amount': 1
            }
        }

        transfer_broadcast_result = broadcast_operation(
            echo=self.echo,
            operation_ids=self.echo.config.operation_ids.TRANSFER,
            props=transfer_props
        )

        self.assertNotIn('error', transfer_broadcast_result)

    def test_transfer_without_fee(self):
        transfer_props = {
            'from': _from,
            'to': _to,
            'amount': {
                'asset_id': '1.3.0',
                'amount': 1
            }
        }

        transfer_broadcast_result = broadcast_operation(
            echo=self.echo,
            operation_ids=self.echo.config.operation_ids.TRANSFER,
            props=transfer_props
        )

        self.assertNotIn('error', transfer_broadcast_result)

    def test_transfer_double(self):
        transfer_props = {
            'fee': {
                'asset_id': '1.3.0',
                'amount': 20
            },
            'from': _from,
            'to': _to,
            'amount': {
                'asset_id': '1.3.0',
                'amount': 1
            }
        }

        second_transfer_props = deepcopy(transfer_props)
        del second_transfer_props['fee']

        ids = [self.echo.config.operation_ids.TRANSFER for _ in range(2)]
        props = [transfer_props, second_transfer_props]

        transfer_broadcast_result = broadcast_operation(
            echo=self.echo,
            operation_ids=ids,
            props=props
        )

        self.assertNotIn('error', transfer_broadcast_result)

    def test_asset_create(self):
        asset_create_props = {
            "issuer": _from,
            "symbol": get_random_asset_symbol(),
            "precision": 5,
            'common_options': {
                'max_supply': 1000000000000000,
                'market_fee_percent': 0,
                'max_market_fee': 1000000000000000,
                'issuer_permissions': 78,
                'flags': 0,
                'core_exchange_rate': {
                    'base': {
                        'amount': 10,
                        'asset_id': '1.3.0',
                    },
                    'quote': {
                        'amount': 2,
                        'asset_id': '1.3.1',
                    }
                },
                'whitelist_authorities': [],
                'blacklist_authorities': [],
                'whitelist_markets': [],
                'blacklist_markets': [],
                'description': '',
            },
            'is_prediction_market': False
        }

        asset_create_broadcast_result = broadcast_operation(
            echo=self.echo,
            operation_ids=self.echo.config.operation_ids.ASSET_CREATE,
            props=asset_create_props
        )
        with self.subTest(asset_create_broadcast_result=asset_create_broadcast_result):
            asset_issue_broadcast_result = subtest_asset_issue(self.echo, asset_create_broadcast_result)
            self.assertNotIn('error', asset_issue_broadcast_result)

    def test_create_contract(self):
        create_contract_props = {
            "fee": {
                "amount": 500,
                "asset_id": "1.3.0"
            },
            "registrar": _from,
            "value": {
                "amount": 10,
                "asset_id": "1.3.0"
            },
            "code": """608060405234801561001057600080fd5b50610159806100206000396000f300608060405260043610610041576000357c0100000000000000000000000000000000000000000000000000000000
        900463ffffffff168063dce4a44714610046575b600080fd5b34801561005257600080fd5b50610087600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050
        610102565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156100c75780820151818401526020810190506100ac565b50505050905090810190601f16801561
        00f45780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6060813b6040519150601f19601f602083010116820160405280825280600060208401853c5091905056
        00a165627a7a723058200267c4df2b48c4dcdf7624d6d794c3669951bb5142e4bca582a01465c3cdbd670029""",
            "eth_accuracy": False
        }

        create_contract_broadcast_result = broadcast_operation(
            echo=self.echo,
            operation_ids=self.echo.config.operation_ids.CREATE_CONTRACT,
            props=create_contract_props
        )

        try:
            create_contract_result_id = create_contract_broadcast_result['trx']['operation_results'][0][1]
            with self.subTest(create_contract_result_id=create_contract_result_id):
                call_contract_broadcast_result = subtest_call_contract(self.echo, create_contract_result_id)
                self.assertNotIn('error', call_contract_broadcast_result)
        except KeyError:
            raise Exception('Contract not created')

    def test_account_create(self):
        private_base58, public_base58, private_hex, public_hex = get_keys()
        account_create_props = {
            "ed_key": public_base58,
            "registrar": _from,
            "referrer": _from,
            "referrer_percent": 1,
            "name": random_string(),
            "active": {
                "weight_threshold": 1,
                "account_auths": [],
                "key_auths": [[public_base58, 1]],
            },
            "options": {
                "memo_key": 'ECHO59St8wBpta2ZREBnA3dQQTVFBrEcx5UK12Tm5geG7kv7Hwyzyc',
                "voting_account": '1.2.5',
                "delegating_account": '1.2.5',
                "num_committee": 0,
                "votes": []
            },
        }
        try:
            account_create_broadcast_result = broadcast_operation(
                echo=self.echo,
                operation_ids=self.echo.config.operation_ids.ACCOUNT_CREATE,
                props=account_create_props
            )
            self.assertNotIn('error', account_create_broadcast_result)
        except RPCError as e:
            try:
                self.assertIn('Only Lifetime members may register an account.', str(e))
            except AssertionError:
                self.assertIn('Insufficient Balance', str(e))

    def test_account_upgrade(self):
        account_upgrade_props = {
            "account_to_upgrade": _from,
            "upgrade_to_lifetime_member": True
        }

        try:
            account_upgrade_broadcast_result = broadcast_operation(
                echo=self.echo,
                operation_ids=self.echo.config.operation_ids.ACCOUNT_UPGRADE,
                props=account_upgrade_props
            )
            self.assertNotIn('error', account_upgrade_broadcast_result)
        except RPCError as e:
            try:
                self.assertIn('Insufficient Balance', str(e))
            except AssertionError:
                self.assertIn('Unable to upgrade account', str(e))

    def test_account_update(self):
        private_base58, public_base58, private_hex, public_hex = get_keys()
        account_update_props = {
            "account": _from,
            "ed_key": "DET269oGvqUJgyMQcR7sbGjJbyAEBQhiD5SUq3XKnZuLinN",
            "new_options": {
                "memo_key": "ECHO1111111111111111111111111111111114T1Anm",
                "voting_account": "1.2.5",
                "delegating_account": "1.2.8",
                "num_committee": 0,
                "votes": [],
            }
        }
        account_update_broadcast_result = broadcast_operation(
            echo=self.echo,
            operation_ids=self.echo.config.operation_ids.ACCOUNT_UPDATE,
            props=account_update_props
        )
        self.assertNotIn('error', account_update_broadcast_result)
