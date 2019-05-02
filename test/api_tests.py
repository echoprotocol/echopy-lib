import unittest
from .fixtures import connect_echo, disconnect_echo
from echopy.echoapi.ws.exceptions import RPCError


class ApiTest(unittest.TestCase):
    def setUp(self):
        self.echo = connect_echo()

    def tearDown(self):
        disconnect_echo(self.echo)

    # ASSET API TESTS
    def test_get_asset_holders(self):
        api = self.echo.api.asset

        get_asset_holders_result = api.get_asset_holders('1.3.0', 1, 1)

        self.assertIsInstance(get_asset_holders_result, list)
        self.assertTrue(len(get_asset_holders_result))
        self.assertIsInstance(get_asset_holders_result[0], dict)
        self.assertTrue(len(get_asset_holders_result[0].keys()))
        self.assertIsInstance(get_asset_holders_result[0]['name'], str)
        self.assertIsInstance(get_asset_holders_result[0]['account_id'], str)
        self.assertIsInstance(get_asset_holders_result[0]['amount'], str)

    def test_get_asset_holders_count(self):
        api = self.echo.api.asset

        get_asset_holders_count_result = api.get_asset_holders_count('1.3.0')

        self.assertIsInstance(get_asset_holders_count_result, int)

    def test_get_all_asset_holders(self):
        api = self.echo.api.asset

        get_all_asset_holders_result = api.get_all_asset_holders()

        self.assertIsInstance(get_all_asset_holders_result, list)
        self.assertTrue(len(get_all_asset_holders_result))
        self.assertIsInstance(get_all_asset_holders_result[0], dict)
        self.assertTrue(len(get_all_asset_holders_result[0].keys()))
        self.assertIsInstance(get_all_asset_holders_result[0]['asset_id'], str)
        self.assertIsInstance(get_all_asset_holders_result[0]['count'], int)

    # DATABASE API TESTS
    def test_get_chain_properties(self):
        api = self.echo.api.database

        get_chain_properties_result = api.get_chain_properties()

        self.assertIsInstance(get_chain_properties_result, dict)
        self.assertIsInstance(get_chain_properties_result['chain_id'], str)
        self.assertIsInstance(get_chain_properties_result['id'], str)
        self.assertIsInstance(get_chain_properties_result['immutable_parameters'], dict)
        self.assertTrue(len(get_chain_properties_result['immutable_parameters'].keys()))

    def test_get_global_properties(self):
        api = self.echo.api.database

        get_global_properties_result = api.get_global_properties()

        self.assertIsInstance(get_global_properties_result, dict)
        self.assertIsInstance(get_global_properties_result['active_committee_members'], list)
        self.assertIsInstance(get_global_properties_result['active_witnesses'], list)
        self.assertIsInstance(get_global_properties_result['id'], str)
        self.assertIsInstance(get_global_properties_result['next_available_vote_id'], int)
        self.assertIsInstance(get_global_properties_result['parameters'], dict)
        self.assertTrue(len(get_global_properties_result['parameters'].keys()))

    def test_get_config(self):
        api = self.echo.api.database

        get_config_result = api.get_config()

        self.assertIsInstance(get_config_result, dict)
        self.assertTrue(len(get_config_result.keys()))

    def test_get_chain_id(self):
        api = self.echo.api.database

        get_chain_id_result = api.get_chain_id()

        self.assertIsInstance(get_chain_id_result, str)
        self.assertTrue(len(get_chain_id_result))

    def test_get_dynamic_global_properties(self):
        api = self.echo.api.database

        get_dynamic_global_properties_result = api.get_dynamic_global_properties()

        self.assertIsInstance(get_dynamic_global_properties_result, dict)
        self.assertTrue(len(get_dynamic_global_properties_result.keys()))

    def test_get_block(self):
        api = self.echo.api.database
        block_number = 20

        get_block_result = api.get_block(block_number)

        self.assertIsInstance(get_block_result, dict)
        self.assertTrue(len(get_block_result.keys()))

    def test_get_transaction(self):
        api = self.echo.api.database
        block_number = 55320
        transaction_index = 0

        get_transaction_result = api.get_transaction(block_number, transaction_index)

        self.assertIsInstance(get_transaction_result, dict)
        self.assertTrue(len(get_transaction_result.keys()))

    def test_get_accounts(self):
        api = self.echo.api.database
        account_id1 = '1.2.5'
        account_id2 = '1.2.6'
        accounts = [account_id1, account_id2]

        get_accounts_result = api.get_accounts(accounts)

        self.assertIsInstance(get_accounts_result, list)
        self.assertEqual(len(get_accounts_result), len(accounts))
        for i in range(len(accounts)):
            self.assertTrue(len(get_accounts_result[i]))

    def test_get_full_accounts_result(self):
        api = self.echo.api.database
        account_id1 = '1.2.5'
        account_id2 = '1.2.6'
        accounts = [account_id1, account_id2]

        get_full_accounts_result = api.get_full_accounts(accounts, False)

        self.assertIsInstance(get_full_accounts_result, list)
        self.assertEqual(len(get_full_accounts_result), len(accounts))
        for i in range(len(accounts)):
            self.assertIsInstance(get_full_accounts_result[i], list)
            self.assertEqual(len(get_full_accounts_result[i]), 2)
            self.assertIsInstance(get_full_accounts_result[i][0], str)
            self.assertTrue(len(get_full_accounts_result[i][0]))
            self.assertIsInstance(get_full_accounts_result[i][1], dict)
            self.assertTrue(len(get_full_accounts_result[i][1].keys()))

    def test_get_account_count(self):
        api = self.echo.api.database

        get_account_count_result = api.get_account_count()

        self.assertIsInstance(get_account_count_result, int)

    def test_lookup_asset_symbols(self):
        api = self.echo.api.database
        asset_key = 'ECHO'
        assets = [asset_key]

        lookup_asset_symbols_result = api.lookup_asset_symbols(assets)

        self.assertIsInstance(lookup_asset_symbols_result, list)
        self.assertEqual(len(lookup_asset_symbols_result), len(assets))
        for i in range(len(assets)):
            self.assertIsInstance(lookup_asset_symbols_result[i], dict)
            self.assertTrue(len(lookup_asset_symbols_result[i].keys()))

    def test_get_assets(self):
        api = self.echo.api.database
        asset_id = '1.3.0'
        assets = [asset_id]

        get_assets_result = api.get_assets(assets)

        self.assertIsInstance(get_assets_result, list)
        self.assertEqual(len(get_assets_result), len(assets))
        for i in range(len(assets)):
            self.assertIsInstance(get_assets_result[i], dict)
            self.assertTrue(len(get_assets_result[i].keys()))

    def test_get_objects(self):
        api = self.echo.api.database
        account_id1 = '1.2.5'
        asset_id = '1.3.0'
        witness_id = '1.6.0'
        objects = [account_id1, asset_id, witness_id]

        get_objects_result = api.get_objects(objects)

        self.assertIsInstance(get_objects_result, list)
        self.assertEqual(len(get_objects_result), len(objects))
        for i in range(len(objects)):
            self.assertIsInstance(get_objects_result[i], dict)
            self.assertTrue(len(get_objects_result[i].keys()))

    def test_get_committee_members(self):
        api = self.echo.api.database
        committee_member = '1.5.1'
        committee_members = [committee_member]

        get_committee_members_result = api.get_committee_members(committee_members)

        self.assertIsInstance(get_committee_members_result, list)
        self.assertEqual(len(get_committee_members_result), len(committee_members))
        for i in range(len(committee_members)):
            self.assertIsInstance(get_committee_members_result[i], dict)
            self.assertTrue(len(get_committee_members_result[i].keys()))
            self.assertEqual(get_committee_members_result[i]['id'], committee_members[i])

    def test_get_account_by_name(self):
        api = self.echo.api.database
        account_name = 'nathan'

        get_account_by_name_result = api.get_account_by_name(account_name)

        self.assertIsInstance(get_account_by_name_result, dict)
        self.assertTrue(len(get_account_by_name_result.keys()))

    def test_lookup_accounts(self):
        api = self.echo.api.database

        lower_bound_name = 't'
        count = 2

        lookup_accounts_result = api.lookup_accounts(lower_bound_name, count)

        self.assertIsInstance(lookup_accounts_result, list)
        self.assertEqual(len(lookup_accounts_result), count)
        for i in range(count):
            self.assertIsInstance(lookup_accounts_result[i], list)
            self.assertIsInstance(lookup_accounts_result[i][0], str)
            self.assertIsInstance(lookup_accounts_result[i][1], str)
            self.assertEqual(lookup_accounts_result[i][1][:3], '1.2')

    def test_list_assets(self):
        api = self.echo.api.database

        lower_bound_symbol = 'E'
        count = 2

        list_assets_result = api.list_assets(lower_bound_symbol, count)

        self.assertIsInstance(list_assets_result, list)
        self.assertEqual(len(list_assets_result), count)
        for i in range(count):
            self.assertIsInstance(list_assets_result[i], dict)
            self.assertTrue(len(list_assets_result[i].keys()))

    def test_get_block_header(self):
        api = self.echo.api.database

        # block_number = 20

        get_block_header_result = api.get_block_header(20)

        self.assertIsInstance(get_block_header_result, dict)
        self.assertTrue(len(get_block_header_result.keys()))

    def test_get_contract(self):
        api = self.echo.api.database

        contract_id = '1.16.0'

        get_contract_result = api.get_contract(contract_id)

        self.assertIsInstance(get_contract_result, list)
        self.assertIsInstance(get_contract_result[0], int)
        self.assertIsInstance(get_contract_result[1], dict)
        self.assertIn('code', get_contract_result[1])
        self.assertIsInstance(get_contract_result[1]['code'], str)
        if 'storage' in get_contract_result[1]:
            self.assertIsInstance(get_contract_result[1]['storage'], list)
            for elem in get_contract_result[1]['storage']:
                self.assertIsInstance(elem, list)
                self.assertEqual(len(elem), 2)
                self.assertIsInstance(elem[0], str)
                self.assertIsInstance(elem[1], list)
                self.assertEqual(len(elem[1]), 2)
                for part in elem[1]:
                    self.assertIsInstance(part, str)

    def test_get_contracts(self):
        api = self.echo.api.database

        contract_id = '1.16.0'
        contracts = [contract_id]

        get_contracts_result = api.get_contracts(contracts)

        self.assertIsInstance(get_contracts_result, list)
        self.assertEqual(len(get_contracts_result), len(contracts))
        self.assertIsInstance(get_contracts_result[0], dict)
        self.assertTrue(len(get_contracts_result[0].keys()))

    def test_lookup_vote_ids(self):
        api = self.echo.api.database

        committee_vote_id = '0:1'
        vote_ids = [committee_vote_id]

        lookup_vote_ids_result = api.lookup_vote_ids(vote_ids)

        self.assertIsInstance(lookup_vote_ids_result, list)
        self.assertEqual(len(lookup_vote_ids_result), len(vote_ids))
        for i in range(len(vote_ids)):
            self.assertIsInstance(lookup_vote_ids_result[i], dict)
            self.assertTrue(len(lookup_vote_ids_result[i]))
            self.assertEqual(lookup_vote_ids_result[i]['vote_id'], vote_ids[i])

    def test_get_committee_member_by_account(self):
        api = self.echo.api.database

        account_id = '1.2.6'

        get_committee_member_by_account_result = api.get_committee_member_by_account(account_id)

        self.assertIsInstance(get_committee_member_by_account_result, dict)
        self.assertTrue(len(get_committee_member_by_account_result.keys()))
        self.assertEqual(get_committee_member_by_account_result['committee_member_account'], account_id)

    def test_get_sidechain_transfers(self):
        api = self.echo.api.database

        ethereum_address = '17A686Cc581e0582e0213Ec49153Af6c1941CAc7'

        get_sidechain_transfers_result = api.get_sidechain_transfers(ethereum_address)

        self.assertIsInstance(get_sidechain_transfers_result, list)

    # REGISTRATION API TESTS
    def test_register_account(self):
        api = self.echo.api.registration

        account_name = 'test101'
        owner_key = 'ECHO59St8wBpta2ZREBnA3dQQTVFBrEcx5UK12Tm5geG7kv7Hwyzyc'
        active_key = 'ECHO59St8wBpta2ZREBnA3dQQTVFBrEcx5UK12Tm5geG7kv7Hwyzyc'
        memo = 'ECHO59St8wBpta2ZREBnA3dQQTVFBrEcx5UK12Tm5geG7kv7Hwyzyc'
        echo_rand_key = 'DET3vw54ewEd7G8aKGHSzC5QbKpGhWEaRH1EvscHMbwZNVW'

        with self.assertRaises(RPCError) as cm:
            api.register_account(account_name, owner_key, active_key, memo, echo_rand_key)

        # exception = cm.exception
        self.assertIn('Assert Exception', str(cm.exception))
        self.assertIn('Account with this name already exists', str(cm.exception))

    # HISTORY API TESTS
    def test_get_account_history(self):
        api = self.echo.api.history

        account_id = '1.2.2'
        limit = 3

        get_account_history_result = api.get_account_history(account_id, limit=limit)

        self.assertIsInstance(get_account_history_result, list)
        if len(get_account_history_result):
            self.assertLessEqual(len(get_account_history_result), limit)
            for history_point in get_account_history_result:
                self.assertIsInstance(history_point, dict)
                self.assertTrue(len(history_point.keys()))

    def test_get_relative_account_history(self):
        api = self.echo.api.history

        account_id = '1.2.22'
        start = stop = 0
        limit = 3

        get_relative_account_history_result = api.get_relative_account_history(account_id, stop, limit, start)

        self.assertIsInstance(get_relative_account_history_result, list)
        if len(get_relative_account_history_result):
            self.assertLessEqual(len(get_relative_account_history_result), limit)
            for history_point in get_relative_account_history_result:
                self.assertIsInstance(history_point, dict)
                self.assertTrue(len(history_point.keys()))

    def test_get_account_history_operations(self):
        api = self.echo.api.history

        account_id = '1.2.22'
        operation_id = 0
        limit = 3

        get_account_history_operations_result = api.get_account_history_operations(account_id,
                                                                                   operation_id,
                                                                                   limit=limit)

        self.assertIsInstance(get_account_history_operations_result, list)
        if len(get_account_history_operations_result):
            self.assertLessEqual(len(get_account_history_operations_result), limit)
            for history_point in get_account_history_operations_result:
                self.assertIsInstance(history_point, dict)
                self.assertTrue(len(history_point.keys()))

    def test_get_contract_history(self):
        api = self.echo.api.history

        contract_id = '1.16.0'
        limit = 3

        get_contract_history_result = api.get_contract_history(contract_id, limit=limit)

        self.assertIsInstance(get_contract_history_result, list)
        if len(get_contract_history_result):
            self.assertLessEqual(len(get_contract_history_result), limit)
            for i in range(limit):
                self.assertIsInstance(get_contract_history_result[i], dict)
                self.assertTrue(len(get_contract_history_result[i].keys()))
