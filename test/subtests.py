from .fixtures import broadcast_operation, _from, _to


def subtest_call_contract(echo, create_contract_result_id):
    if not create_contract_result_id:
        raise Exception('Contract not created')

    object_id_start_index = create_contract_result_id.rfind('.') + 1
    create_contract_result_id = create_contract_result_id[:object_id_start_index] +\
        str(int(create_contract_result_id[object_id_start_index:]) - 1)
    contract_id = int(echo.api.database.get_contract_result(create_contract_result_id)
                      [1]['exec_res']['new_address'][2:], 16)

    call_contract_props = {
        "registrar": _from,
        "value": {
            "amount": 0,
            "asset_id": "1.3.0"
        },
        "code": '86be3f80' + '0000000000000000000000000000000000000000000000000000000000000001',
        "callee": '1.14.' + str(contract_id)
    }

    call_contract_broadcast_result = broadcast_operation(
        echo=echo,
        operation_ids=echo.config.operation_ids.CALL_CONTRACT,
        props=call_contract_props
    )

    return call_contract_broadcast_result


def subtest_asset_issue(echo, create_asset_result):
    if not create_asset_result:
        raise Exception('Asset not created')

    asset_id = create_asset_result['trx']['operation_results'][0][1]

    asset_issue_props = {
        "issuer": _from,
        "asset_to_issue": {
            "amount": 100,
            "asset_id": asset_id
        },
        "issue_to_account": _to
    }

    asset_issue_broadcast_result = broadcast_operation(
        echo=echo,
        operation_ids=echo.config.operation_ids.ASSET_ISSUE,
        props=asset_issue_props
    )
    return asset_issue_broadcast_result
