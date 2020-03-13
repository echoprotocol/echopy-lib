import re

idRegex = re.compile('^(0|([1-9]\d*\.)){2}(0|([1-9]\d*))$')
accountIdRegex = re.compile('^1\.2\.(0|[1-9]\d*)$')
assetIdRegex = re.compile('^1\.3\.(0|[1-9]\d*)$')
forceSettlementIdRegex = re.compile('^1\.4\.[1-9]\d*$')
committeeMemberIdRegex = re.compile('^1\.5\.(0|[1-9]\d*)$')
witnessIdRegex = re.compile('^1\.6\.(0|[1-9]\d*)$')
limitOrderIdRegex = re.compile('^1\.7\.[1-9]\d*$')
callOrderIdRegex = re.compile('^1\.8\.[1-9]\d*$')
customIdRegex = re.compile('^1\.9\.[1-9]\d*$')
proposalIdRegex = re.compile('^1\.10\.[1-9]\d*$')
operationHistoryIdRegex = re.compile('^1\.11\.(0|[1-9]\d*)$')
withdrawPermissionIdRegex = re.compile('^1\.12\.[1-9]\d*$')
vestingBalanceIdRegex = re.compile('^1\.13\.[1-9]\d*$')
workerIdRegex = re.compile('^1\.14\.[1-9]\d*$')
balanceIdRegex = re.compile('^1\.15\.[1-9]\d*$')
contractIdRegex = re.compile('^1\.16\.(0|[1-9]\d*)$')
contractResultIdRegex = re.compile('^1\.17\.[1-9]\d*$')
dynamicGlobalObjectIdRegex = re.compile('^2.1.0$')
dynamicAssetDataIdRegex = re.compile('^2\.3\.(0|[1-9]\d*)$')
bitAssetIdRegex = re.compile('^2\.4\.(0|[1-9]\d*)$')
accountBalanceIdRegex = re.compile('^2\.5\.[1-9]\d*$')
accountStatisticsIdRegex = re.compile('^2\.6\.[1-9]\d*$')
transactionIdRegex = re.compile('^2\.7\.[1-9]\d*$')
blockSummaryIdRegex = re.compile('^2\.8\.[1-9]\d*$')
accountTransactionHistoryIdRegex = re.compile('^2\.9\.[1-9]\d*$')
hexRegex = re.compile('^[0-9a-fA-F]+')
bytecodeRegex = re.compile('^[\da-fA-F]{8}([\da-fA-F]{64})*$')
voteIdTypeRegex = re.compile('^[0-3]{1}:[0-9]+')


def is_object_id(v):
    return bool(idRegex.match(v) and len(v.split('.')) == 3)


def is_string(v):
    if type(v) != str:
        raise ValueError("Entered value is not string")


def is_account_id(v):
    if is_string(v):
        return bool(accountIdRegex.match(v))


def is_asset_id(v):
    if is_string(v):
        return bool(assetIdRegex.match(v))


def is_forse_settlement_id(v):
    if is_string(v):
        return bool(forceSettlementIdRegex.match(v))


def is_committee_member_id(v):
    if is_string(v):
        return bool(committeeMemberIdRegex.match(v))


def is_witness_id(v):
    if is_string(v):
        return bool(witnessIdRegex.match(v))


def is_limit_order_id(v):
    if is_string(v):
        return bool(limitOrderIdRegex.match(v))


def is_call_order_id(v):
    if is_string(v):
        return bool(callOrderIdRegex.match(v))


def is_custom_id(v):
    if is_string(v):
        return bool(customIdRegex.match(v))


def is_proposal_id(v):
    if is_string(v):
        return bool(proposalIdRegex.match(v))


def is_operation_history_id(v):
    if is_string(v):
        return bool(operationHistoryIdRegex.match(v))


def is_withdraw_permission_id(v):
    if is_string(v):
        return bool(withdrawPermissionIdRegex.match(v))


def is_vesting_balance_id(v):
    if is_string(v):
        return bool(vestingBalanceIdRegex.match(v))


def is_worker_id(v):
    if is_string(v):
        return bool(workerIdRegex.match(v))


def is_balance_id(v):
    if is_string(v):
        return bool(balanceIdRegex.match(v))


def is_contract_id(v):
    if is_string(v):
        return bool(contractIdRegex.match(v))


def is_contract_result_id(v):
    if is_string(v):
        return bool(contractResultIdRegex.match(v))


def is_dynamic_global_object_id(v):
    if is_string(v):
        return bool(dynamicGlobalObjectIdRegex.match(v))


def is_dynamic_asset_data_id(v):
    if is_string(v):
        return bool(dynamicAssetDataIdRegex.match(v))


def is_bit_asset_id(v):
    if is_string(v):
        return bool(bitAssetIdRegex.match(v))


def is_account_balance_id(v):
    if is_string(v):
        return bool(accountBalanceIdRegex.match(v))


def is_account_statistics_id(v):
    if is_string(v):
        return bool(accountStatisticsIdRegex.match(v))


def is_transaction_id(v):
    if is_string(v):
        return bool(transactionIdRegex.match(v))


def is_block_summary_id(v):
    if is_string(v):
        return bool(blockSummaryIdRegex.match(v))


def is_account_transaction_history_id(v):
    if is_string(v):
        return bool(accountTransactionHistoryIdRegex.match(v))


def is_hex(v):
    if is_string(v):
        return bool(hexRegex.match(v))


def is_bytecode(v):
    if is_string(v):
        return bool(bytecodeRegex.match(v))


def is_bytes(v, length):
    return is_hex(v) and len(v) == length * 2


def is_vote_id(v):
    if is_string(v):
        return bool(voteIdTypeRegex.match(v))


def is_uint(v, x):
    v = int(v)
    if v < 0 or v >= 2**x:
        raise ValueError("Entered value is greater than this type may contain")
    try:
        return bool(v)
    except:
        raise ValueError("Value is not integer")


def is_int(v, x):
    v = abs(int(v))
    if v > 2**x:
        raise ValueError("Entered value is greater than this type may contain")
    try:
        return bool(v)
    except:
        raise ValueError("Value is not integer")


def is_uint8(v):
    return is_uint(v, 8)


def is_uint16(v):
    return is_uint(v, 16)


def is_uint32(v):
    return is_uint(v, 32)


def is_uint64(v):
    return is_uint(v, 64)


def is_int64(v):
    return is_int(v, 64)


def is_asset_name(v):
    return bool(v is not None and len(v.split(".")) <= 2 and len(v) >= 3 and len(v) <= 16 and re.match('^[A-Z][A-Z\d\.]*[A-Z]$', v))

NAME_MIN_LENGTH = 3
NAME_MAX_LENGTH = 63


def is_account_name(v):
    if not is_string(v):
        return False
    if v is None:
        return False
    if len(v) < NAME_MIN_LENGTH or len(v) > NAME_MAX_LENGTH:
        return False

    ref = v.split(".")

    for label in ref:
        if not bool(re.match('^[a-z][a-z0-9-]*[a-z\d]$', label)) or bool(re.match('.*--.*', label)):
            return False
    return True


def is_ripemd160(v):
    return is_hex(v) and len(v) == 40


def check_account_name(value):
    if value is None or len(value) == 0:
        raise ValueError('Acount nane should not be empyt.')
    if len(value) < NAME_MIN_LENGTH or len(value) > NAME_MAX_LENGTH:
        raise ValueError("Account name should be from 3 to 63.")
    for label in range(value.split('.')):
        if not re.match('^[~a-z]', label):
            raise ValueError("Each account segment should start with a letter.")
        if not re.match('^[~a-z0-9-]*$', label):
            raise ValueError("Each account segment should have only letter, digits or dashes.")
        if re.match('.*--.*', label):
            raise ValueError("Each account segment should have only one dash in a row.")
        if not re.match('[a-z0-9]$', label):
            raise ValueError('Each account segment should end with a letter or digit.')
        if len(label) < NAME_MIN_LENGTH:
            raise ValueError('Each account segment should be longer.')
    return 0


def is_operation_id(v):
    return is_uint8(v) and v < 49


def is_echo_rand_key(v, echoRandPrefix='ECHO'):
    if not is_string(v) or len(v) != 44 + len(echoRandPrefix):  # config.ECHORAND_KEY_LENGTH = 44
        return False
    prefix = v[0:len(echoRandPrefix)]
    return echoRandPrefix == prefix


def is_public_key(v, addressPrefix="ECHO"):
    if is_string(v) or len(v) != 44 + len(addressPrefix):  # config.ECHORAND_KEY_LENGTH = 44
        return False
    prefix = v[0:len(addressPrefix)]
    return addressPrefix == prefix
