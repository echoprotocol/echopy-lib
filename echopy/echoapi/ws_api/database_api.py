# -*- coding: utf-8 -*-
class DatabaseApi:
    def __init__(self, db):
        self.db = db

    async def get_objects(self, object_ids):
        return await self.db.rpcexec("get_objects", [object_ids])

    async def set_subscribe_callback(self, callback, notify_remove_create):
        return await self.db.rpcexec("set_subscribe_callback"), [callback, notify_remove_create]

    async def set_pending_transaction_callback(self, callback):
        return await self.db.rpcexec("set_pending_transaction_callback", [callback])

    async def set_block_applied_callback(self, callback):
        return await self.db.rpcexec("set_block_applied_callback", [callback])

    async def cancel_all_subscriptions(self):
        return await self.db.rpcexec('cancel_all_subscriptions', [])

    async def get_block_header(self, block_num):
        return await self.db.rpcexec('get_block_header', [block_num])

    async def get_block(self, block_num):
        return await self.db.rpcexec('get_block', [block_num])

    async def get_transaction(self, block_num, transaction_index):
        return await self.db.rpcexec('get_transaction', [block_num, transaction_index])

    async def get_chain_properties(self):
        return await self.db.rpcexec('get_chain_properties', [])

    async def get_global_properties(self):
        return await self.db.rpcexec('get_global_properties', [])

    async def get_config(self):
        return await self.db.rpcexec('get_config', [])

    async def get_chain_id(self):
        return await self.db.rpcexec('get_chain_id', [])

    async def get_dynamic_global_properties(self):
        return await self.db.rpcexec('get_dynamic_global_properties', [])

    async def get_key_references(self, keys):
        return await self.db.rpcexec('get_key_references', [keys])

    async def get_accounts(self, account_ids):
        return await self.db.rpcexec('get_accounts', [account_ids])

    async def get_full_accounts(self, account_name_or_ids, subscribe):
        return await self.db.rpcexec("get_full_accounts", [account_name_or_ids, subscribe])

    async def get_account_by_name(self, account_name):
        return await self.db.rpcexec('get_account_by_name', [account_name])

    async def get_account_references(self, account_id):
        return await self.db.rpcexec('get_account_references', [account_id])

    async def lookup_account_names(self, account_names):
        return await self.db.rpcexec('lookup_account_names', [account_names])

    async def lookup_accounts(self, lower_bound_name, limit):
        return await self.db.rpcexec('lookup_accounts', [lower_bound_name, limit])

    async def get_account_count(self):
        return await self.db.rpcexec('get_account_count', [])

    async def get_account_balances(self, account_id, asset_ids):
        return await self.db.rpcexec('get_account_balances', [account_id, asset_ids])

    async def get_named_account_balances(self, account_name, asset_ids):
        return await self.db.rpcexec('get_named_account_balances', [account_name, asset_ids])

    async def get_vested_balances(self, object_ids):
        return await self.db.rpcexec('get_vested_balances', [object_ids])

    async def get_vesting_balances(self, account_id):
        return await self.db.rpcexec('get_vesting_balances', [account_id])

    async def get_assets(self, asset_ids):
        return await self.db.rpcexec('get_assets', [asset_ids])

    async def list_assets(self, lower_bound_symbol, limit):
        return await self.db.rpcexec('list_assets', [lower_bound_symbol, limit])

    async def lookup_asset_symbols(self, symbols_or_ids):
        return await self.db.rpcexec('lookup_asset_symbols', [symbols_or_ids])

    async def get_order_book(self, base_asset_name, quote_asset_name, depth=50):
        return await self.db.rpcexec('get_order_book', [base_asset_name, quote_asset_name, depth])

    async def get_limit_orders(self, baseasset_id, quoteasset_id, limit):
        return await self.db.rpcexec('get_limit_orders', [baseasset_id, quoteasset_id, limit])

    async def get_call_orders(self, asset_id, limit):
        return await self.db.rpcexec('get_call_orders', [asset_id, limit])

    async def get_settle_orders(self, asset_id, limit):
        return await self.db.rpcexec('get_settle_orders', [asset_id, limit])

    async def get_margin_positions(self, account_id):
        return await self.db.rpcexec('get_margin_positions', [account_id])

    async def subscribe_to_market(self, callback, baseasset_id, quoteasset_id):
        return await self.db.rpcexec('subscribe_to_market', [callback, baseasset_id, quoteasset_id])

    async def unsubscribe_to_market(self, baseasset_id, quoteasset_id):
        return await self.db.rpcexec('unsubscribe_to_market', [baseasset_id, quoteasset_id])

    async def get_ticker(self, base_asset_name, quote_asset_name):
        return await self.db.rpcexec('get_ticker', [base_asset_name, quote_asset_name])

    async def get_24_volume(self, base_asset_name, quote_asset_name):
        return await self.db.rpcexec('get_24_volume', [base_asset_name, quote_asset_name])

    async def get_trade_history(self, base_asset_name, quote_asset_name, start, stop, limit):
        return await self.db.rpcexec('get_trade_history', [base_asset_name, quote_asset_name, start, stop, limit])

    async def get_witnesses(self, witness_ids):
        return await self.db.rpcexec('get_witnesses', [witness_ids])

    async def get_witness_by_account(self, account_id):
        return await self.db.rpcexec('get_witness_by_account', [account_id])

    async def lookup_witness_accounts(self, lower_bound_name, limit):
        return await self.db.rpcexec('lookup_witness_accounts', [lower_bound_name, limit])

    async def get_witness_count(self):
        return await self.db.rpcexec("get_witness_count", [])

    async def get_committee_members(self, committee_member_ids):
        return await self.db.rpcexec('get_committee_members', [committee_member_ids])

    async def get_committee_member_by_account(self, account_id):
        return await self.db.rpcexec('get_committee_member_by_account', [account_id])

    async def lookup_committee_member_accounts(self, lower_bound_name, limit):
        return await self.db.rpcexec('lookup_committee_member_accounts', [lower_bound_name, limit])

    async def get_workers_by_account(self, account_id):
        return await self.db.rpcexec('get_workers_by_account', [account_id])

    async def lookup_vote_ids(self, votes):
        return await self.db.rpcexec('lookup_vote_ids', [votes])

    async def get_transaction_hex(self, transaction):
        return await self.db.rpcexec('get_transaction_hex', [transaction])

    async def get_required_signatures(self, transaction, available_keys):
        return await self.db.rpcexec('get_required_signatures', [transaction, available_keys])

    async def get_potential_signatures(self, transaction):
        return await self.db.rpcexec('get_potential_signatures', [transaction])

    async def get_potential_address_signatures(self, transaction):
        return await self.db.rpcexec('get_potential_address_signatures', [transaction])

    async def verify_authority(self, transaction):
        return await self.db.rpcexec('verify_authority', [transaction])

    async def verify_account_authority(self, account_name_or_id, signers):
        return await self.db.rpcexec('verify_account_authority', [account_name_or_id, signers])

    async def validate_transaction(self, transaction):
        return await self.db.rpcexec('validate_transaction', [transaction])

    async def get_required_fees(self, operations, asset_id):
        return await self.db.rpcexec('get_required_fees', [operations, asset_id])

    async def get_proposed_transactions(self, account_name_or_id):
        return await self.db.rpcexec('get_proposed_transactions', [account_name_or_id])

    async def get_all_contracts(self):
        return await self.db.rpcexec('get_all_contracts', [])

    async def get_contract_logs(self, contract_id, from_block, to_block):
        return await self.db.rpcexec('get_contract_logs', [contract_id, from_block, to_block])

    async def subscribe_contract_logs(self, callback, contract_id, from_block, to_block):
        return await self.db.rpcexec('subscribe_contract_logs', [callback, contract_id, from_block, to_block])

    async def get_contract_result(self, resultcontract_id):
        return await self.db.rpcexec('get_contract_result', [resultcontract_id])

    async def get_contract(self, contract_id):
        return await self.db.rpcexec('get_contract', [contract_id])

    async def call_contract_no_changing_state(self, contract_id, account_id, asset_id, bytecode):
        return await self.db.rpcexec('call_contract_no_changing_state',
                                     [contract_id, account_id, asset_id, bytecode])

    async def get_contracts(self, contract_ids):
        return await self.db.rpcexec('get_contracts', [contract_ids])

    async def get_contract_balances(self, contract_id):
        return await self.db.rpcexec('get_contract_balances', [contract_id])

    async def get_recent_transaction_by_id(self, transaction_id):
        return await self.db.rpcexec('get_recent_transaction_by_id', [transaction_id])

    async def get_sidechain_transfers(self, reciever):
        return await self.db.rpcexec('get_sidechain_transfers', [reciever])
