import hashlib
import hmac
from _hashlib import compare_digest
from datetime import datetime

import six
# from jwt import InvalidAlgorithmError

from config import settings


def __int_to_base36(i):
    """Convert an integer to a base36 string."""
    char_set = "0123456789abcdefghijklmnopqrstuvwxyz"
    if i < 0:
        raise ValueError("Negative base36 conversion input.")
    if i < 36:
        return char_set[i]
    b36 = ""
    while i != 0:
        i, n = divmod(i, 36)
        b36 = char_set[n] + b36
    return b36


def __base36_to_int(s):
    """base36 string Convert to an integer ."""
    if len(s) > 13:
        raise ValueError("Base36 input too large")
    return int(s, 36)


def _salted_hmac(key_salt, value, secret, *, algorithm="sha256"):
    key_salt = key_salt.encode('utf-8')
    secret = secret.encode('utf-8')

    hasher = hashlib.sha256
    # try:
    #     hasher = getattr(hashlib, algorithm)
    # except AttributeError as e:
    #     raise InvalidAlgorithmError(
    #         "%r is not an algorithm accepted by the hashlib module." % algorithm
    #     ) from e

    key = hasher(key_salt + secret).digest()
    return hmac.new(key, msg=value.encode('utf-8'), digestmod=hasher)


def _make_token_with_timestamp(user, timestamp, secret):
    text = six.text_type(user.id) + user.password + six.text_type(user.updated_at) + secret
    ts_b36 = __int_to_base36(timestamp)
    hash_string = _salted_hmac(ts_b36, text, secret).hexdigest()[::2]
    return "%s-%s" % (ts_b36, hash_string)


def _num_seconds(dt):
    return int((dt - datetime(2001, 1, 1)).total_seconds())


def _now():
    return datetime.now()


def make_token(user):
    return _make_token_with_timestamp(
        user,
        _num_seconds(_now()),
        settings.SECRET_KEY
    )


def check_token(user, token) -> bool:
    try:
        ts_b36, _ = token.split("-")
    except ValueError:
        return False
    try:
        ts = __base36_to_int(ts_b36)
    except ValueError:
        return False

    if (_num_seconds(_now()) - ts) > settings.ACTIVATE_TOKEN_TIMEOUT:
        return False

    return compare_digest(
        _make_token_with_timestamp(user, ts, settings.SECRET_KEY),
        token
    )
