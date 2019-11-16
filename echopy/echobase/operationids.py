#: Operation ids
ops = [
    "transfer",
    "transfer_to_address",
    "override_transfer",
    "account_create",
    "account_update",
    "account_whitelist",
    "account_address_create",
    "asset_create",
    "asset_update",
    "asset_update_bitasset",
    "asset_update_feed_producers",
    "asset_issue",
    "asset_reserve",
    "asset_fund_fee_pool",
    "asset_publish_feed",
    "asset_claim_fees",
    "proposal_create",
    "proposal_update",
    "proposal_delete",
    "committee_member_create",
    "committee_member_update",
    "committee_member_update_global_parameters",
    "committee_member_activate",
    "committee_member_deactivate",
    "committee_frozen_balance_deposit",
    "committee_frozen_balance_withdraw",
    "vesting_balance_create",
    "vesting_balance_withdraw",
    "balance_claim",
    "balance_freeze",
    "balance_unfreeze",
    "contract_create",
    "contract_call",
    "contract_internal_create",
    "contract_internal_call",
    "contract_selfdestruct",
    "contract_update",
    "contract_fund_pool",
    "contract_whitelist",
    "sidechain_eth_create_address",
    "sidechain_eth_approve_address",
    "sidechain_eth_deposit",
    "sidechain_eth_withdraw",
    "sidechain_eth_approve_withdraw",
    "sidechain_issue",
    "sidechain_burn",
    "sidechain_erc20_register_token",
    "sidechain_erc20_deposit_token",
    "sidechain_erc20_withdraw_token",
    "sidechain_erc20_approve_token_withdraw",
    "sidechain_erc20_issue",
    "sidechain_erc20_burn",
    "sidechain_btc_create_address",
    "sidechain_btc_create_intermediate_deposit",
    "sidechain_btc_intermediate_deposit",
    "sidechain_btc_deposit",
    "sidechain_btc_withdraw",
    "sidechain_btc_aggregate",
    "sidechain_btc_approve_aggregate",
    "block_reward"
]
operations = {o: ops.index(o) for o in ops}
