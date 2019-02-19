import unittest
from echo import Echo
import string
import random


class Test(unittest.TestCase):

    def test_create_contract(self):
        def test_call_contract(echo, contract_result_id):
            if not contract_result_id:
                raise Exception('Contract not created')
            contract_id = int(echo.api.database.get_contract_result(contract_result_id)[1]['exec_res']['new_address'][2:], 16)

            props = {
                "registrar": "1.2.68",
                "value": {
                    "amount": 0,
                    "asset_id": "1.3.0"
                },
                "gasPrice": 0,
                "gas": 1e7,
                "code": '86be3f80' + '0000000000000000000000000000000000000000000000000000000000000001',
                "callee": '1.16.' + str(contract_id)
            }
            tx = echo.create_transaction()
            tx = tx.add_operation(name=48, props=props)
            tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
            tx.sign()
            tx.broadcast()
            print('Create and Call contract tests passed')

        echo = Echo(node='ws://195.201.164.54:6311')
        props = {
            "fee": {
                "amount": 100,
                "asset_id": "1.3.0"
            },
            "registrar": "1.2.68",
            "value": {
                "amount": 0,
                "asset_id": "1.3.0"
            },
            "gasPrice": 0,
            "gas": 1e7,
            "code": """608060405234801561001057600080fd5b50610159806100206000396000f300608060405260043610610041576000357c0100000000000000000000000000000000000000000000000000000000
        900463ffffffff168063dce4a44714610046575b600080fd5b34801561005257600080fd5b50610087600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050
        610102565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156100c75780820151818401526020810190506100ac565b50505050905090810190601f16801561
        00f45780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6060813b6040519150601f19601f602083010116820160405280825280600060208401853c5091905056
        00a165627a7a723058200267c4df2b48c4dcdf7624d6d794c3669951bb5142e4bca582a01465c3cdbd670029""",
            "eth_accuracy": False
        }
        tx = echo.create_transaction()
        tx.add_operation(name=47, props=props)
        tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
        tx.sign()
        create_contract_result = tx.broadcast()
        try:
            create_contract_result_id = create_contract_result['trx']['operation_results'][0][1]
            with self.subTest(echo=echo, create_contract_result_id=create_contract_result_id):
                test_call_contract(echo, create_contract_result_id)
                self.assertTrue(True)
        except KeyError:
            raise Exception('Contract not created')

    def test_transfer(self):

        echo = Echo(node='ws://195.201.164.54:6311')
        tx = echo.create_transaction()

        props = {
            'fee': {
                'asset_id': '1.3.0',
                'amount': 20
            },
            'from': '1.2.68',
            'to': '1.2.733',
            'amount': {
                'asset_id': '1.3.0',
                'amount': 1
            }
        }

        tx = tx.add_operation(name=0, props=props)
        tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
        tx.sign()
        tx.broadcast()
        print('Transfer test passed')

    def test_create_asset(self):

        asset_symbol_length = random.randint(4, 10)
        asset_symbol = ''.join(random.choice(string.ascii_uppercase) for _ in range(asset_symbol_length))
        echo = Echo(node='ws://195.201.164.54:6311')
        tx = echo.create_transaction()

        props = {
            "issuer": "1.2.68",
            "symbol": asset_symbol,
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

        tx = tx.add_operation(name=10, props=props)
        tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
        tx.sign()
        tx.broadcast()
        print('Create Asset test passed')
