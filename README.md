# Python Library for Graphene

![](https://img.shields.io/pypi/v/graphenelib.svg?style=for-the-badge)
![](https://img.shields.io/github/downloads/xeroc/python-graphenelib/total.svg?style=for-the-badge)
![](https://img.shields.io/pypi/pyversions/graphenelib.svg?style=for-the-badge)
![](https://img.shields.io/pypi/l/graphenelib.svg?style=for-the-badge)
![](https://cla-assistant.io/readme/badge/xeroc/python-graphenelib)

**Stable**

[![Travis master](https://travis-ci.org/xeroc/python-graphenelib.png?branch=master)](https://travis-ci.org/xeroc/python-graphenelib)
[![docs master](https://readthedocs.org/projects/python-graphenelib/badge/?version=latest)](http://python-graphenelib.readthedocs.io/en/latest/)
[![codecov](https://codecov.io/gh/xeroc/python-graphenelib/branch/master/graph/badge.svg)](https://codecov.io/gh/xeroc/python-graphenelib)


**Develop**

[![Travis develop](https://travis-ci.org/xeroc/python-graphenelib.png?branch=develop)](https://travis-ci.org/xeroc/python-graphenelib)
[![docs develop](https://readthedocs.org/projects/python-graphenelib/badge/?version=develop)](http://python-graphenelib.readthedocs.io/en/develop/)
[![codecov develop](https://codecov.io/gh/xeroc/python-graphenelib/branch/develop/graph/badge.svg)](https://codecov.io/gh/xeroc/python-graphenelib)

---
## Documentation

Visit the [pygraphenelib website](http://docs.pygraphenelib.com/en/latest/) for in depth documentation on this Python library.

## Installation


### Manual installation:

    $ git clone https://gitlab.pixelplex.by/645.echo/echopy-lib.git
    $ cd echopy-lib
    $ python3 setup.py install


## Current status of operations

| Operation | Operation status |
| --- | --- | 
| account_create | <ul><li>[x] </li></ul>  |
| account_update | <ul><li>[ ] </li></ul>  |
| account_whitelist | <ul><li>[ ] </li></ul>  |
| account_upgrade | <ul><li>[ ] </li></ul>  |
| account_transfer | <ul><li>[ ] </li></ul>  |
| assert | <ul><li>[ ] </li></ul>  |
| asset_create | <ul><li>[ ] </li></ul>  |
| asset_global_settle | <ul><li>[ ] </li></ul>  |
| asset_settle | <ul><li>[ ] </li></ul>  |
| asset_settle_cancel | <ul><li>[ ] </li></ul>  |
| asset_fund_fee_pool | <ul><li>[ ] </li></ul>  |
| asset_update_bitasset | <ul><li>[ ] </li></ul>  |
| asset_update_feed_producers | <ul><li>[ ] </li></ul>  |
| asset_publish_feed | <ul><li>[ ] </li></ul>  |
| asset_issue | <ul><li>[ ] </li></ul>  |
| asset_reserve | <ul><li>[ ] </li></ul>  |
| asset_claim_fees | <ul><li>[ ] </li></ul>  |
| balance_claim | <ul><li>[ ] </li></ul>  |
| commitee_member_create | <ul><li>[ ] </li></ul>  |
| commitee_member_update | <ul><li>[ ] </li></ul>  |
| commitee_member_update_global_parameters | <ul><li>[ ] </li></ul>  |
| transfer_to_blind | <ul><li>[ ] </li></ul>  |
| transfer_from_blind | <ul><li>[ ] </li></ul>  |
| blind_transfer | <ul><li>[ ] </li></ul>  |
| create_contract | <ul><li>[ ] </li></ul>  |
| call_contract | <ul><li>[ ] </li></ul>  |
| contract_transfer | <ul><li>[ ] </li></ul>  |
| custom_operation | <ul><li>[ ] </li></ul>  |
| fba_distribute | <ul><li>[ ] </li></ul>  |
| limit_order_create | <ul><li>[ ] </li></ul>  |
| limit_order_cancel | <ul><li>[ ] </li></ul>  |
| call_order_update | <ul><li>[ ] </li></ul>  |
| fill_order | <ul><li>[ ] </li></ul>  |
| bid_collateral | <ul><li>[ ] </li></ul>  |
| execute_bid | <ul><li>[ ] </li></ul>  |
| proposal_create | <ul><li>[ ] </li></ul>  |
| proporsal_update | <ul><li>[ ] </li></ul>  |
| proposal_delete | <ul><li>[ ] </li></ul>  |
| transfer | <ul><li>[ ] </li></ul>  |
| override_transfer | <ul><li>[ ] </li></ul>  |
| vesting_balance_create | <ul><li>[ ] </li></ul>  |
| vesting_balance_withdraw | <ul><li>[ ] </li></ul>  |
| withdraw_permission_create | <ul><li>[ ] </li></ul>  |
| withdraw_permission_update | <ul><li>[ ] </li></ul>  |
| withdraw_permission_claim | <ul><li>[ ] </li></ul>  |
| withdraw_permission_delete | <ul><li>[ ] </li></ul>  |
| witness_create | <ul><li>[ ] </li></ul>  |
| witness_update | <ul><li>[ ] </li></ul>  |
| worker_create | <ul><li>[ ] </li></ul>  |

## Current status of Apis methods

### Login API 

| Methods | Status |
| --- | --- | 
| login | <ul><li>[ ] </li></ul>  |
| network_broadcast | <ul><li>[ ] </li></ul>  |
| database | <ul><li>[ ] </li></ul>  |
| history | <ul><li>[ ] </li></ul>  |
| crypto | <ul><li>[ ] </li></ul>  |

### Asset API

| Methods | Status |
| --- | --- | 
| get_asset_holders | <ul><li>[ ] </li></ul>  |
| get_asset_holders_count | <ul><li>[ ] </li></ul>  |
| get_all_asset_holders | <ul><li>[ ] </li></ul>  |

### Database API

| Methods | Status |
| --- | --- | 
| get_objects | <ul><li>[ ] </li></ul>  |
| set_subscribe_callback | <ul><li>[ ] </li></ul>  |
| set_pending_transaction_callback | <ul><li>[ ] </li></ul>  |
| set_block_applied_callback | <ul><li>[ ] </li></ul>  |
| cancel_all_subscriptions | <ul><li>[ ] </li></ul>  |
| get_block_header | <ul><li>[ ] </li></ul>  |
| get_block | <ul><li>[ ] </li></ul>  |
| get_transaction | <ul><li>[ ] </li></ul>  |
| get_recent_transaction_by_id | <ul><li>[ ] </li></ul>  |
| get_chain_properties | <ul><li>[ ] </li></ul>  |
| get_global_properties | <ul><li>[ ] </li></ul>  |
| get_config | <ul><li>[ ] </li></ul>  |
| get_chain_id | <ul><li>[ ] </li></ul>  |
| get_dynamic_global_properties | <ul><li>[ ] </li></ul>  |
| get_key_references | <ul><li>[ ] </li></ul>  |
| get_accounts | <ul><li>[ ] </li></ul>  |
| get_full_accounts | <ul><li>[ ] </li></ul>  |
| get_account_by_name | <ul><li>[ ] </li></ul>  |
| get_account_references | <ul><li>[ ] </li></ul>  |
| lookup_account_names | <ul><li>[ ] </li></ul>  |
| lookup_accounts | <ul><li>[ ] </li></ul>  |
| get_account_count | <ul><li>[ ] </li></ul>  |
| get_account_balances | <ul><li>[ ] </li></ul>  |
| get_named_account_balances | <ul><li>[ ] </li></ul>  |
| get_balance_objects | <ul><li>[ ] </li></ul>  |
| get_vested_balances | <ul><li>[ ] </li></ul>  |
| get_vesting_balances | <ul><li>[ ] </li></ul>  |
| get_assets | <ul><li>[ ] </li></ul>  |
| list_assets | <ul><li>[ ] </li></ul>  |
| lookup_asset_symbols | <ul><li>[ ] </li></ul>  |
| get_order_book | <ul><li>[ ] </li></ul>  |
| get_limit_orders | <ul><li>[ ] </li></ul>  |
| get_call_orders | <ul><li>[ ] </li></ul>  |
| get_settle_orders | <ul><li>[ ] </li></ul>  |
| get_margin_positions | <ul><li>[ ] </li></ul>  |
| subscribe_to_market | <ul><li>[ ] </li></ul>  |
| unsubscribe_from_market | <ul><li>[ ] </li></ul>  |
| get_ticker | <ul><li>[ ] </li></ul>  |
| get_24_volume | <ul><li>[ ] </li></ul>  |
| get_trade_history | <ul><li>[ ] </li></ul>  |
| get_witnesses | <ul><li>[ ] </li></ul>  |
| get_witness_by_account | <ul><li>[ ] </li></ul>  |
| lookup_witness_accounts | <ul><li>[ ] </li></ul>  |
| get_witness_count | <ul><li>[ ] </li></ul>  |
| get_committee_members | <ul><li>[ ] </li></ul>  |
| get_committee_member_by_account | <ul><li>[ ] </li></ul>  |
| lookup_committee_member_accounts | <ul><li>[ ] </li></ul>  |
| get_workers_by_account | <ul><li>[ ] </li></ul>  |
| lookup_vote_ids | <ul><li>[ ] </li></ul>  |
| get_transaction_hex | <ul><li>[ ] </li></ul>  |
| get_required_signatures | <ul><li>[ ] </li></ul>  |
| get_potential_signatures | <ul><li>[ ] </li></ul>  |
| get_potential_address_signatures | <ul><li>[ ] </li></ul>  |
| verify_authority | <ul><li>[ ] </li></ul>  |
| verify_account_authority | <ul><li>[ ] </li></ul>  |
| validate_transaction | <ul><li>[ ] </li></ul>  |
| get_required_fees | <ul><li>[ ] </li></ul>  |
| get_proposed_transactions | <ul><li>[ ] </li></ul>  |
| get_all_contracts | <ul><li>[ ] </li></ul>  |
| get_contract_logs | <ul><li>[ ] </li></ul>  |
| subscribe_contract_logs | <ul><li>[ ] </li></ul>  |
| get_contract_result | <ul><li>[ ] </li></ul>  |
| get_contract | <ul><li>[ ] </li></ul>  |
| call_contract_no_changing_state | <ul><li>[ ] </li></ul>  |
| get_contracts | <ul><li>[ ] </li></ul>  |
| get_contract_balances | <ul><li>[ ] </li></ul>  |

### Network broadcast API

| Methods | Status |
| --- | --- | 
| broadcast_transaction | <ul><li>[ ] </li></ul>  |
| broadcast_block | <ul><li>[ ] </li></ul>  |
| broadcast_transaction_with_callback | <ul><li>[ ] </li></ul>  |
| broadcast_transaction_synchronous | <ul><li>[ ] </li></ul>  |

### History API

| Methods | Status |
| --- | --- | 
| get_account_history | <ul><li>[ ] </li></ul>  |
| get_relative_account_history | <ul><li>[ ] </li></ul>  |
| get_account_history_operations | <ul><li>[ ] </li></ul>  |
| get_contract_history | <ul><li>[ ] </li></ul>  |

### Network broadcast API

| Methods | Status |
| --- | --- | 
| broadcast_transaction | <ul><li>[ ] </li></ul>  |
| broadcast_block | <ul><li>[ ] </li></ul>  |
| broadcast_transaction_with_callback | <ul><li>[ ] </li></ul>  |
| broadcast_transaction_synchronous | <ul><li>[ ] </li></ul>  |

### Registration API

| Methods | Status |
| --- | --- | 
| register_account | <ul><li>[ ] </li></ul>  |


## Contributing

python-bitshares welcomes contributions from anyone and everyone. Please
see our [guidelines for contributing](CONTRIBUTING.md) and the [code of
conduct](CODE_OF_CONDUCT.md).

### Discussion and Developers

Discussions around development and use of this library can be found in a
[dedicated Telegram Channel](https://t.me/pybitshares)

### License

A copy of the license is available in the repository's
[LICENSE](LICENSE.txt) file.
