import datetime
import uuid
import jwt
import hashlib
import pprint


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


def cookies2dict(cookies):
    cookies_list = list(map(lambda item: item.split('='), cookies.split(';')))

    cookies_dict = {item[0]: item[1] for item in cookies_list}

    return cookies_dict


def compare_food_list(list_src, list_dst):
    flag = False
    for src, dst in zip(list_src, list_dst):
        if src['foodName'] == dst['foodName']:
            flag = True
        else:
            flag = False

    return flag


def date2str(date: datetime.date):
    return date.strftime('%Y-%m-%d %H:%M:%S')


def str2date(date_str: str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')


if __name__ == '__main__':
    cookies = 'device_uuid=!83a9448e-7f9e-4d8d-ad73-50e95f27d752;uuid_update=true;shopCategory=food;JSESSIONID=h50rrtb3e6qv1ny6ynftof4;acctId=187417283;token=014A56OA2Z6LiViQqRQUWj1SRJ3mzzc-rckZQsR7thWE*;wmPoiId=20815629;isOfflineSelfOpen=0;city_id=310100;isChain=0;ignore_set_router_proxy=false;region_id=1000310100;region_version=1710840050;bsid=meNN-Gi_ZSt5ZinIOcE6Ss5ItfKkF29e_7rjk0eNs5yV3gYYsY6zzP26yi4YUSem24r1f3xireAxmQbcQwy3yw;city_location_id=310100;location_id=310113;has_not_waimai_poi=0;cityId=520200;provinceId=520000;set_info=%7B%22wmPoiId%22%3A%2220815629%22%2C%22region_id%22%3A%221000310100%22%2C%22region_version%22%3A1710840050%7D;wpush_server_url=wss://wpush.meituan.com;pushToken=014A56OA2Z6LiViQqRQUWj1SRJ3mzzc-rckZQsR7thWE*;setPrivacyTime=1_20240513;logan_session_token=jk94i3zb1p4di313qarv'
    pprint.pprint(cookies2dict(cookies))
