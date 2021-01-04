import hmac
import hashlib


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
