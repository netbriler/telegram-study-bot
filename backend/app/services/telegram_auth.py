import hmac
import hashlib


def verify_authorization(data: dict, api_token: str) -> bool:
    sorted_data = dict(sorted(data.items(), key=lambda x: x[0].lower()))
    del sorted_data['hash']

    data_check_string = bytes('\n'.join('='.join(_) for _ in sorted_data.items()), 'utf-8')
    secret_key = hashlib.sha256(api_token.encode('utf-8')).digest()

    hmac_string = hmac.new(secret_key, data_check_string, hashlib.sha256).hexdigest()

    return hmac_string == data['hash']
