# -*- coding: utf-8 -*-
class DatabaseApi:
    def __init__(self, db):
        self.db = db

    # Objects
    async def get_objects(self, object_ids):
        return await self.db.rpcexec(
            'get_objects',
            [object_ids]
        )

    # Subscriptions
    async def set_subscribe_callback(self, callback, clear_filter):
        return await self.db.rpcexec(
            'set_subscribe_callback',
            [callback, clear_filter]
        )

    async def set_pending_transaction_callback(self, callback):
        return await self.db.rpcexec(
            'set_pending_transaction_callback',
            [callback]
        )

    async def set_block_applied_callback(self, callback):
        return await self.db.rpcexec(
            'set_block_applied_callback',
            [callback]
        )

    async def cancel_all_subscriptions(self):
        return await self.db.rpcexec(
            'cancel_all_subscriptions',
            []
        )

    # Block and transactions
    async def get_block_header(self, block_num):
        return await self.db.rpcexec(
            'get_block_header',
            [block_num]
        )

    async def get_block_header_batch(self, block_nums):
        return await self.db.rpcexec(
            'get_block_header_batch',
            [block_nums]
        )

    async def get_block(self, block_num):
        return await self.db.rpcexec(
            'get_block',
            [block_num]
        )

    async def get_block_tx_number(self, block_id):
        return await self.db.rpcexec(
            'get_block_tx_number',
            [block_id]
        )

    async def get_block_virtual_ops(self, block_num):
        return await self.db.rpcexec(
            'get_block_virtual_ops',
            [block_num]
        )

    async def get_transaction(self, block_num, trx_in_block):
        return await self.db.rpcexec(
            'get_transaction',
            [block_num, trx_in_block]
        )

    async def get_recent_transaction_by_id(self, transaction_id):
        return await self.db.rpcexec(
            'get_recent_transaction_by_id',
            [transaction_id]
        )

    # Globals
    async def get_chain_properties(self):
        return await self.db.rpcexec(
            'get_chain_properties',
            []
        )

    async def get_global_properties(self):
        return await self.db.rpcexec(
            'get_global_properties',
            []
        )

    async def get_config(self):
        return await self.db.rpcexec(
            'get_config',
            []
        )

    async def get_chain_id(self):
        return await self.db.rpcexec(
            'get_chain_id',
            []
        )

    async def get_dynamic_global_properties(self):
        return await self.db.rpcexec(
            'get_dynamic_global_properties',
            []
        )

    # Keys
    async def get_key_references(self, keys):
        return await self.db.rpcexec(
            'get_key_references',
            [keys]
        )

    async def is_public_key_registered(self, key):
        return await self.db.rpcexec(
            'is_public_key_registered',
            [key]
        )

    # Accounts
    async def get_accounts(self, account_ids):
        return await self.db.rpcexec(
            'get_accounts',
            [account_ids]
        )

    async def get_full_accounts(self, names_or_ids, subscribe):
        return await self.db.rpcexec(
            'get_full_accounts',
            [names_or_ids, subscribe]
        )

    async def get_account_by_name(self, name):
        return await self.db.rpcexec(
            'get_account_by_name',
            [name]
        )

    async def get_account_references(self, account_id):
        return await self.db.rpcexec(
            'get_account_references',
            [account_id]
        )

    async def lookup_account_names(self, account_names):
        return await self.db.rpcexec(
            'lookup_account_names',
            [account_names]
        )

    async def lookup_accounts(self, lower_bound_name, limit):
        return await self.db.rpcexec(
            'lookup_accounts',
            [lower_bound_name, limit]
        )

    async def get_account_addresses(self, account_id, from_block_num, limit):
        return await self.db.rpcexec(
            'get_account_addresses',
            [account_id, from_block_num, limit]
        )

    async def get_account_by_address(self, address):
        return await self.db.rpcexec(
            'get_account_by_address',
            [address]
        )

    async def get_evm_addresses(self, account_id):
        return await self.db.rpcexec(
            'get_evm_addresses',
            [account_id]
        )

    async def get_account_count(self):
        return await self.db.rpcexec(
            'get_account_count',
            []
        )

    # Contracts
    async def get_contract(self, contract_id):
        return await self.db.rpcexec(
            'get_contract',
            [contract_id]
        )

    async def get_contracts(self, contract_ids):
        return await self.db.rpcexec(
            'get_contracts',
            [contract_ids]
        )

    async def get_contract_logs(self, callback, contracts=None, topics=None, from_block=None, to_block=None):
        opts = {}
        if contracts is not None:
            opts["contracts"] = contracts
        if topics is not None:
            opts["topics"] = topics
        if from_block is not None:
            opts["from_block"] = from_block
        if to_block is not None:
            opts["to_block"] = to_block

        return await self.db.rpcexec(
            'get_contract_logs',
            [callback, opts]
        )

    async def subscribe_contracts(self, contracts_ids):
        return await self.db.rpcexec(
            'subscribe_contracts',
            [contracts_ids]
        )

    async def subscribe_contract_logs(self, callback_id, callback, contract_id):
        return await self.db.rpcexec(
            'subscribe_contract_logs',
            [callback_id, callback, contract_id]
        )

    async def unsubscribe_contract_logs(self, callback_id):
        return await self.db.rpcexec(
            'unsubscribe_contract_logs',
            [callback_id]
        )

    async def get_contract_result(self, contract_result_id):
        return await self.db.rpcexec(
            'get_contract_result',
            [contract_result_id]
        )

    async def call_contract_no_changing_state(self, contract_id, caller, value, code):
        return await self.db.rpcexec(
            'call_contract_no_changing_state',
            [contract_id, caller, value, code]
        )

    # Balances
    async def get_account_balances(self, account_id, assets):
        return await self.db.rpcexec(
            'get_account_balances',
            [account_id, assets]
        )

    async def get_contract_balances(self, contract_id):
        return await self.db.rpcexec(
            'get_contract_balances',
            [contract_id]
        )

    async def get_named_account_balances(self, name, assets):
        return await self.db.rpcexec(
            'get_named_account_balances',
            [name, assets]
        )

    async def get_balance_objects(self, keys):
        return await self.db.rpcexec(
            'get_balance_objects',
            [keys]
        )

    async def get_vested_balances(self, objs):
        return await self.db.rpcexec(
            'get_vested_balances',
            [objs]
        )

    async def get_vesting_balances(self, account_id):
        return await self.db.rpcexec(
            'get_vesting_balances',
            [account_id]
        )

    async def get_frozen_balances(self, account_id):
        return await self.db.rpcexec(
            'get_frozen_balances',
            [account_id]
        )

    async def get_committee_frozen_balance(self, committee_member_id):
        return await self.db.rpcexec(
            'get_committee_frozen_balance',
            [committee_member_id]
        )

    # Assets
    async def get_assets(self, asset_ids):
        return await self.db.rpcexec(
            'get_assets',
            [asset_ids]
        )

    async def list_assets(self, lower_bound_symbol, limit):
        return await self.db.rpcexec(
            'list_assets',
            [lower_bound_symbol, limit]
        )

    async def lookup_asset_symbols(self, symbols_or_ids):
        return await self.db.rpcexec(
            'lookup_asset_symbols',
            [symbols_or_ids]
        )

    # Committee members
    async def get_committee_members(self, committee_member_ids):
        return await self.db.rpcexec(
            'get_committee_members',
            [committee_member_ids]
        )

    async def get_committee_member_by_account(self, account):
        return await self.db.rpcexec(
            'get_committee_member_by_account',
            [account]
        )

    async def lookup_committee_member_accounts(self, lower_bound_name, limit):
        return await self.db.rpcexec(
            'lookup_committee_member_accounts',
            [lower_bound_name, limit]
        )

    async def get_committee_count(self):
        return await self.db.rpcexec(
            'get_committee_count',
            []
        )

    # Authority / validation
    async def get_transaction_hex(self, trx):
        return await self.db.rpcexec(
            'get_transaction_hex',
            [trx]
        )

    async def get_required_signatures(self, trx, available_keys):
        return await self.db.rpcexec(
            'get_required_signatures',
            [trx, available_keys]
        )

    async def get_potential_signatures(self, trx):
        return await self.db.rpcexec(
            'get_potential_signatures',
            [trx]
        )

    async def verify_authority(self, trx):
        return await self.db.rpcexec(
            'verify_authority',
            [trx]
        )

    async def verify_account_authority(self, name_or_id, signers):
        return await self.db.rpcexec(
            'verify_account_authority',
            [name_or_id, signers]
        )

    async def validate_transaction(self, trx):
        return await self.db.rpcexec(
            'validate_transaction',
            [trx]
        )

    async def get_required_fees(self, operations, asset_id):
        return await self.db.rpcexec(
            'get_required_fees',
            [operations, asset_id]
        )

    # Proposed transactions
    async def get_proposed_transactions(self, account_id):
        return await self.db.rpcexec(
            'get_proposed_transactions',
            [account_id]
        )

    # Sidechain
    async def get_account_deposits(self, account, deposit_type):
        return await self.db.rpcexec(
            'get_account_deposits',
            [account, deposit_type]
        )

    async def get_account_withdrawals(self, account, deposit_type):
        return await self.db.rpcexec(
            'get_account_withdrawals',
            [account, deposit_type]
        )

    # Sidechain Ethereum
    async def get_eth_address(self, account):
        return await self.db.rpcexec(
            'get_eth_address',
            [account]
        )

    # Sidechain ERC20
    async def get_erc20_token(self, eth_addr):
        return await self.db.rpcexec(
            'get_erc20_token',
            [eth_addr]
        )

    async def check_erc20_token(self, contract_id):
        return await self.db.rpcexec(
            'check_erc20_token',
            [contract_id]
        )

    async def get_erc20_account_deposits(self, account):
        return await self.db.rpcexec(
            'get_erc20_account_deposits',
            [account]
        )

    async def get_erc20_account_withdrawals(self, account):
        return await self.db.rpcexec(
            'get_erc20_account_withdrawals',
            [account]
        )

    # Sidechain Bitcoin
    async def get_btc_address(self, account):
        return await self.db.rpcexec(
            'get_btc_address',
            [account]
        )

    async def get_btc_deposit_script(self, address):
        return await self.db.rpcexec(
            'get_btc_deposit_script',
            [address]
        )

    # Contract Feepool
    async def get_contract_pool_balance(self, contract_id):
        return await self.db.rpcexec(
            'get_contract_pool_balance',
            [contract_id]
        )

    async def get_contract_pool_whitelist(self, contract_id):
        return await self.df.rpcexec(
            'get_contract_pool_whitelist',
            [contract_id]
        )
