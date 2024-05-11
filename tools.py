import datetime
import uuid
import jwt
import hashlib


def api_response(code, msg, data={}, total=0):
    return {
        'code': code,
        'msg': msg,
        'data': data,
        'total': total
    }


def generate_unique_string(length=32, prefix="", suffix=""):
    """
    Generate a unique string using UUID and timestamp.

    Args:
        length (int): The desired length of the unique string (default: 10).
        prefix (str): An optional prefix to add to the string.
        suffix (str): An optional suffix to add to the string.

    Returns:
        str: The generated unique string.
    """

    random_id = str(uuid.uuid4())[:length]
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_string = f"{prefix}{random_id}{timestamp}{suffix}"

    return unique_string


def generate_jwt(user_id, username, secret_key, algorithm="HS256"):
    payload = {
        'user_id': user_id,
        'username': username,
        'iat': datetime.datetime.utcnow().timestamp(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    }
    return jwt.encode(payload, secret_key, algorithm=algorithm)


def md5(data):
    _md5 = hashlib.md5()
    _md5.update(data.encode())

    return _md5.hexdigest()
