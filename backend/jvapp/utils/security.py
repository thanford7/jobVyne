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
    hash_string = get_hash_string(make_hash_value(user, user_key, timestamp))
    if user_key:
        return f'{ts_b36}-{user_key}-{hash_string}'
    return f'{ts_b36}-{hash_string}'


def get_hash_string(text):
    return salted_hmac(
        key_salt,
        text,
        secret=settings.SECRET_KEY,
        algorithm='sha256',
    ).hexdigest()[::2]  # Limit to shorten the URL.


def make_hash_value(user, user_key, timestamp):
    if user_key:
        return f'{user.pk}{timestamp}{getattr(user, user_key)}'
    return f'{user.pk}{timestamp}'


def get_user_key_from_token(token):
    return token.split('-')[1]


def check_user_token(user, token):

    if not (user and token):
        return False

    # Parse the token
    token_bits = token.split("-")
    if len(token_bits) == 2:
        ts_b36 = token_bits[0]
        user_key = None
    elif len(token_bits) == 3:
        ts_b36, user_key, _ = token_bits
    else:
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



## This is NOT cryptographically safe! The intent is just to obfuscate text to make it difficult for a user to guess
HASH_SALT = 'adsklgnsalg239rsfdknasl!($KWLERQ@'
HASH_SHIFT = 6


def get_reversible_hash(text):
    salted_text = ''
    for idx, char in enumerate(text):
        salted_text += char
        if idx and (not idx % 3):
            count = int((idx / 3) % len(HASH_SALT))
            salted_text += HASH_SALT[count]
    hashed_text = ''
    for char in salted_text:
        hashed_text += chr(ord(char) + HASH_SHIFT)
    
    return hashed_text
        
        
def reverse_hash(hash_text):
    unsalted_text = ''
    for idx, char in enumerate(hash_text):
        if idx and (not idx % 4):
            continue
        unsalted_text += char
    
    unhashed_text = ''
    for char in unsalted_text:
        unhashed_text += chr(ord(char) - HASH_SHIFT)
    
    return unhashed_text
