from datetime import datetime

from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.encoding import force_bytes
from django.utils.http import base36_to_int, int_to_base36, urlsafe_base64_decode, urlsafe_base64_encode

key_salt = 'jvapp.util.security.generate_user_token'


def generate_user_token(user, user_key, timestamp=None):
    """Get a token from a discrete value from a user instance
    :param user {JobVyneUser}
    :param user_key: A key attribute from the JobVyneUser model (e.g. email)
    :param timestamp
    :return: Token
    """
    timestamp = timestamp or _num_seconds(datetime.now())
    ts_b36 = int_to_base36(timestamp)
    hash_string = salted_hmac(
        key_salt,
        make_hash_value(user, user_key, timestamp),
        secret=settings.SECRET_KEY,
        algorithm='sha256',
    ).hexdigest()[
                  ::2
                  ]  # Limit to shorten the URL.
    return f'{ts_b36}-{user_key}-{hash_string}'


def make_hash_value(user, user_key, timestamp):
    return f'{user.pk}{timestamp}{getattr(user, user_key)}'


def get_user_key_from_token(token):
    return token.split('-')[1]


def check_user_token(user, user_key, token):

    if not (user and token):
        return False
    # Parse the token
    try:
        ts_b36, _, _ = token.split("-")
    except ValueError:
        return False
    
    try:
        ts = base36_to_int(ts_b36)
    except ValueError:
        return False
    
    # Check that the timestamp/uid has not been tampered with
    if not constant_time_compare(generate_user_token(user, user_key, ts), token):
        return False
    
    # Check the timestamp is within limit.
    if (_num_seconds(datetime.now()) - ts) > settings.PASSWORD_RESET_TIMEOUT:
        return False
    
    return True


def get_uid_from_user(user):
    return urlsafe_base64_encode(force_bytes(user.pk))


def get_user_id_from_uid(uid):
    return urlsafe_base64_decode(uid).decode()


def _num_seconds(dt):
    return int((dt - datetime(2001, 1, 1)).total_seconds())
