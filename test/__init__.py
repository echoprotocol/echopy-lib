import unittest
from .fixtures import connect_echo, disconnect_echo, get_random_asset_symbol, _wif, _from, _to


class Test(unittest.TestCase):

    def test_create_contract(self):

        def test_call_contract(echo, create_contract_result_id):
            if not create_contract_result_id:
                raise Exception('Contract not created')
            contract_id = int(echo.api.database.get_contract_result(create_contract_result_id)[1]['exec_res']['new_address'][2:], 16)

            call_contract_props = {
                "registrar": _from,
                "value": {
                    "amount": 0,
                    "asset_id": "1.3.0"
                },
                "code": '86be3f80' + '0000000000000000000000000000000000000000000000000000000000000001',
                "callee": '1.16.' + str(contract_id)
            }

            tx = echo.create_transaction()
            tx = tx.add_operation(name=echo.config.operation_ids.CALL_CONTRACT, props=call_contract_props)
            tx.sign(_wif)
            call_contract_broadcast_result = tx.broadcast()
            self.assertNotIn('error', call_contract_broadcast_result)

        echo = connect_echo()

        create_contract_props = {
            "fee": {
                "amount": 100,
                "asset_id": "1.3.0"
            },
            "registrar": _from,
            "value": {
                "amount": 0,
                "asset_id": "1.3.0"
            },
            "code": """608060405234801561001057600080fd5b50610159806100206000396000f300608060405260043610610041576000357c0100000000000000000000000000000000000000000000000000000000
        900463ffffffff168063dce4a44714610046575b600080fd5b34801561005257600080fd5b50610087600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050
        610102565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156100c75780820151818401526020810190506100ac565b50505050905090810190601f16801561
        00f45780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6060813b6040519150601f19601f602083010116820160405280825280600060208401853c5091905056
        00a165627a7a723058200267c4df2b48c4dcdf7624d6d794c3669951bb5142e4bca582a01465c3cdbd670029""",
            "eth_accuracy": False
        }

        tx = echo.create_transaction()
        tx.add_operation(name=echo.config.operation_ids.CREATE_CONTRACT, props=create_contract_props)
        tx.sign(_wif)
        create_contract_broadcast_result = tx.broadcast()
        try:
            create_contract_result_id = create_contract_broadcast_result['trx']['operation_results'][0][1]
            with self.subTest(echo=echo, create_contract_result_id=create_contract_result_id):
                test_call_contract(echo, create_contract_result_id)
                disconnect_echo(echo)
                self.assertNotIn('error', create_contract_broadcast_result)
        except KeyError:
            raise Exception('Contract not created')

    def test_transfer(self):
        echo = connect_echo()

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

        tx = echo.create_transaction()
        tx = tx.add_operation(name=echo.config.operation_ids.TRANSFER, props=transfer_props)
        tx.sign(_wif)
        transfer_broadcast_result = tx.broadcast()
        disconnect_echo(echo)
        self.assertNotIn('error', transfer_broadcast_result)

    def test_asset_create(self):
        echo = connect_echo()
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
        tx = echo.create_transaction()
        tx = tx.add_operation(name=echo.config.operation_ids.ASSET_CREATE, props=asset_create_props)
        tx.sign(_wif)
        asset_create_broadcast_result = tx.broadcast()
        disconnect_echo(echo)
        self.assertNotIn('error', asset_create_broadcast_result)
