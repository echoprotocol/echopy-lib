# -*- coding: utf-8 -*-
class DatabaseApi:
    def __init__(self, db):
        self.db = db

    # Objects
    def get_objects(self, object_ids):
        return self.db.rpcexec(
            'get_objects',
            [object_ids]
        )

    # Subscriptions
    def set_subscribe_callback(self, callback, clear_filter):
        return self.db.rpcexec(
            'set_subscribe_callback',
            [callback, clear_filter]
        )

    def set_pending_transaction_callback(self, callback):
        return self.db.rpcexec(
            'set_pending_transaction_callback',
            [callback]
        )

    def set_block_applied_callback(self, callback):
        return self.db.rpcexec(
            'set_block_applied_callback',
            [callback]
        )

    def cancel_all_subscriptions(self):
        return self.db.rpcexec(
            'cancel_all_subscriptions',
            []
        )

    # Block and transactions
    def get_block_header(self, block_num):
        return self.db.rpcexec(
            'get_block_header',
            [block_num]
        )

    def get_block_header_batch(self, block_nums):
        return self.db.rpcexec(
            'get_block_header_batch',
            [block_nums]
        )

    def get_block(self, block_num):
        return self.db.rpcexec(
            'get_block',
            [block_num]
        )

    def get_block_tx_number(self, block_id):
        return self.db.rpcexec(
            'get_block_tx_number',
            [block_id]
        )

    def get_block_virtual_ops(self, block_num):
        return self.db.rpcexec(
            'get_block_virtual_ops',
            [block_num]
        )

    def get_transaction(self, block_num, trx_in_block):
        return self.db.rpcexec(
            'get_transaction',
            [block_num, trx_in_block]
        )

    def get_recent_transaction_by_id(self, transaction_id):
        return self.db.rpcexec(
            'get_recent_transaction_by_id',
            [transaction_id]
        )

    # Globals
    def get_chain_properties(self):
        return self.db.rpcexec(
            'get_chain_properties',
            []
        )

    def get_global_properties(self):
        return self.db.rpcexec(
            'get_global_properties',
            []
        )

    def get_config(self):
        return self.db.rpcexec(
            'get_config',
            []
        )

    def get_chain_id(self):
        return self.db.rpcexec(
            'get_chain_id',
            []
        )

    def get_dynamic_global_properties(self):
        return self.db.rpcexec(
            'get_dynamic_global_properties',
            []
        )

    # Keys
    def get_key_references(self, keys):
        return self.db.rpcexec(
            'get_key_references',
            [keys]
        )

    def is_public_key_registered(self, key):
        return self.db.rpcexec(
            'is_public_key_registered',
            [key]
        )

    # Accounts
    def get_accounts(self, account_ids):
        return self.db.rpcexec(
            'get_accounts',
            [account_ids]
        )

    def get_full_accounts(self, names_or_ids, subscribe):
        return self.db.rpcexec(
            'get_full_accounts',
            [names_or_ids, subscribe]
        )

    def get_account_by_name(self, name):
        return self.db.rpcexec(
            'get_account_by_name',
            [name]
        )

    def get_account_references(self, account_id):
        return self.db.rpcexec(
            'get_account_references',
            [account_id]
        )

    def lookup_account_names(self, account_names):
        return self.db.rpcexec(
            'lookup_account_names',
            [account_names]
        )

    def lookup_accounts(self, lower_bound_name, limit):
        return self.db.rpcexec(
            'lookup_accounts',
            [lower_bound_name, limit]
        )

    def get_account_addresses(self, account_id, from_block_num, limit):
        return self.db.rpcexec(
            'get_account_addresses',
            [account_id, from_block_num, limit]
        )

    def get_account_by_address(self, address):
        return self.db.rpcexec(
            'get_account_by_address',
            [address]
        )

    def get_evm_addresses(self, account_id):
        return self.db.rpcexec(
            'get_evm_addresses',
            [account_id]
        )

    def get_account_count(self):
        return self.db.rpcexec(
            'get_account_count',
            []
        )

    # Contracts
    def get_contract(self, contract_id):
        return self.db.rpcexec(
            'get_contract',
            [contract_id]
        )

    def get_contracts(self, contract_ids):
        return self.db.rpcexec(
            'get_contracts',
            [contract_ids]
        )

    def get_contract_logs(self, callback, contracts=None, topics=None, from_block=None, to_block=None):
        opts = {}
        if contracts is not None:
            opts["contracts"] = contracts
        if topics is not None:
            opts["topics"] = topics
        if from_block is not None:
            opts["from_block"] = from_block
        if to_block is not None:
            opts["to_block"] = to_block

        return self.db.rpcexec(
            'get_contract_logs',
            [callback, opts]
        )

    def subscribe_contracts(self, contracts_ids):
        return self.db.rpcexec(
            'subscribe_contracts',
            [contracts_ids]
        )

    def subscribe_contract_logs(self, callback_id, callback, contract_id):
        return self.db.rpcexec(
            'subscribe_contract_logs',
            [callback_id, callback, contract_id]
        )

    def unsubscribe_contract_logs(self, callback_id):
        return self.db.rpcexec(
            'unsubscribe_contract_logs',
            [callback_id]
        )

    def get_contract_result(self, contract_result_id):
        return self.db.rpcexec(
            'get_contract_result',
            [contract_result_id]
        )

    def call_contract_no_changing_state(self, contract_id, caller, value, code):
        return self.db.rpcexec(
            'call_contract_no_changing_state',
            [contract_id, caller, value, code]
        )

    # Balances
    def get_account_balances(self, account_id, assets):
        return self.db.rpcexec(
            'get_account_balances',
            [account_id, assets]
        )

    def get_contract_balances(self, contract_id):
        return self.db.rpcexec(
            'get_contract_balances',
            [contract_id]
        )

    def get_named_account_balances(self, name, assets):
        return self.db.rpcexec(
            'get_named_account_balances',
            [name, assets]
        )

    def get_balance_objects(self, keys):
        return self.db.rpcexec(
            'get_balance_objects',
            [keys]
        )

    def get_vested_balances(self, objs):
        return self.db.rpcexec(
            'get_vested_balances',
            [objs]
        )

    def get_vesting_balances(self, account_id):
        return self.db.rpcexec(
            'get_vesting_balances',
            [account_id]
        )

    def get_frozen_balances(self, account_id):
        return self.db.rpcexec(
            'get_frozen_balances',
            [account_id]
        )

    def get_committee_frozen_balance(self, committee_member_id):
        return self.db.rpcexec(
            'get_committee_frozen_balance',
            [committee_member_id]
        )

    # Assets
    def get_assets(self, asset_ids):
        return self.db.rpcexec(
            'get_assets',
            [asset_ids]
        )

    def list_assets(self, lower_bound_symbol, limit):
        return self.db.rpcexec(
            'list_assets',
            [lower_bound_symbol, limit]
        )

    def lookup_asset_symbols(self, symbols_or_ids):
        return self.db.rpcexec(
            'lookup_asset_symbols',
            [symbols_or_ids]
        )

    # Committee members
    def get_committee_members(self, committee_member_ids):
        return self.db.rpcexec(
            'get_committee_members',
            [committee_member_ids]
        )

    def get_committee_member_by_account(self, account):
        return self.db.rpcexec(
            'get_committee_member_by_account',
            [account]
        )

    def lookup_committee_member_accounts(self, lower_bound_name, limit):
        return self.db.rpcexec(
            'lookup_committee_member_accounts',
            [lower_bound_name, limit]
        )

    def get_committee_count(self):
        return self.db.rpcexec(
            'get_committee_count',
            []
        )

    # Authority / validation
    def get_transaction_hex(self, trx):
        return self.db.rpcexec(
            'get_transaction_hex',
            [trx]
        )

    def get_required_signatures(self, trx, available_keys):
        return self.db.rpcexec(
            'get_required_signatures',
            [trx, available_keys]
        )

    def get_potential_signatures(self, trx):
        return self.db.rpcexec(
            'get_potential_signatures',
            [trx]
        )

    def verify_authority(self, trx):
        return self.db.rpcexec(
            'verify_authority',
            [trx]
        )

    def verify_account_authority(self, name_or_id, signers):
        return self.db.rpcexec(
            'verify_account_authority',
            [name_or_id, signers]
        )

    def validate_transaction(self, trx):
        return self.db.rpcexec(
            'validate_transaction',
            [trx]
        )

    def get_required_fees(self, operations, asset_id):
        return self.db.rpcexec(
            'get_required_fees',
            [operations, asset_id]
        )

    # Proposed transactions
    def get_proposed_transactions(self, account_id):
        return self.db.rpcexec(
            'get_proposed_transactions',
            [account_id]
        )

    # Sidechain
    def get_account_deposits(self, account, deposit_type):
        return self.db.rpcexec(
            'get_account_deposits',
            [account, deposit_type]
        )

    def get_account_withdrawals(self, account, deposit_type):
        return self.db.rpcexec(
            'get_account_withdrawals',
            [account, deposit_type]
        )

    # Sidechain Ethereum
    def get_eth_address(self, account):
        return self.db.rpcexec(
            'get_eth_address',
            [account]
        )

    # Sidechain ERC20
    def get_erc20_token(self, eth_addr):
        return self.db.rpcexec(
            'get_erc20_token',
            [eth_addr]
        )

    def check_erc20_token(self, contract_id):
        return self.db.rpcexec(
            'check_erc20_token',
            [contract_id]
        )

    def get_erc20_account_deposits(self, account):
        return self.db.rpcexec(
            'get_erc20_account_deposits',
            [account]
        )

    def get_erc20_account_withdrawals(self, account):
        return self.db.rpcexec(
            'get_erc20_account_withdrawals',
            [account]
        )

    # Sidechain Bitcoin
    def get_btc_address(self, account):
        return self.db.rpcexec(
            'get_btc_address',
            [account]
        )

    def get_btc_deposit_script(self, address):
        return self.db.rpcexec(
            'get_btc_deposit_script',
            [address]
        )

    # Contract Feepool
    def get_contract_pool_balance(self, contract_id):
        return self.db.rpcexec(
            'get_contract_pool_balance',
            [contract_id]
        )

    def get_contract_pool_whitelist(self, contract_id):
        return self.df.rpcexec(
            'get_contract_pool_whitelist',
            [contract_id]
        )
