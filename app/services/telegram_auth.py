import hashlib
import hmac
import json
from operator import itemgetter
from urllib.parse import parse_qsl


def check_webapp_signature(token: str, init_data: str) -> bool:
    try:
        parsed_data = dict(parse_qsl(init_data, strict_parsing=True))
    except ValueError:
        return False
    if "hash" not in parsed_data:
        return False
    hash_ = parsed_data.pop("hash")

    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256)
    calculated_hash = hmac.new(
        key=secret_key.digest(), msg=data_check_string.encode(), digestmod=hashlib.sha256
    ).hexdigest()
    return calculated_hash == hash_


def parse_webapp_init_data(
        init_data: str,
        *,
        loads=json.loads,
):
    result = {}
    for key, value in parse_qsl(init_data):
        if (value.startswith("[") and value.endswith("]")) or (
                value.startswith("{") and value.endswith("}")
        ):
            value = loads(value)
        result[key] = value
    return result


def safe_parse_webapp_init_data(
        token: str,
        init_data: str,
        *,
        loads=json.loads,
):
    if check_webapp_signature(token, init_data):
        return parse_webapp_init_data(init_data, loads=loads)
    return False


def verify_authorization(data: dict, api_token: str) -> bool:
    hash = data['hash']
    del data['hash']
    return _generate_hash(data, api_token) == hash


def _generate_hash(data: dict, api_token: str) -> str:
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0].lower()))

    data_check_string = bytes('\n'.join('='.join(_) for _ in sorted_data.items()), 'utf-8')
    secret_key = hashlib.sha256(api_token.encode('utf-8')).digest()

    hmac_string = hmac.new(secret_key, data_check_string, hashlib.sha256).hexdigest()

    return hmac_string
