import datetime
import json
import pprint
import time
from urllib.parse import urlencode, urljoin
import requests
import tools

from comment.models import CommentModel


def get_comments_query_url(cookies: str, comment_type: int, page_size=10):
    cookies_dict = tools.cookies2dict(cookies)

    begin_time = str(int(datetime.datetime.timestamp(datetime.datetime.now() - datetime.timedelta(days=365))))
    end_time = str(int(time.time()))

    comment_api_url = "https://waimaieapp.meituan.com/gw/customer/comment/list"

    params = {
        'ignoreSetRouterProxy': cookies_dict['ignore_set_router_proxy'],
        'acctId': cookies_dict['acctId'],
        'wmPoiId': cookies_dict['wmPoiId'],
        'token': cookies_dict['token'],
        'appType': 3,

        # 0=>全部 1=>好评 2=>中评 3=>差评
        'commScore': comment_type,
        'commType': -1,
        'hasContent': -1,
        'periodType': 1,
        'beginTime': begin_time,
        'endTime': end_time,
        'pageNum': 1,
        'pageSize': page_size,
        'onlyAuditNotPass': 0,
        'source': 0
    }

    query_params = urlencode(params)
    return urljoin(comment_api_url, '?' + query_params)


def get_comments_headers(cookies: str):
    headers = {
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Sec-Ch-Ua-Platform': 'macOS',
        'Host': 'waimaieapp.meituan.com',
        'Refer': 'https://waimaieapp.meituan.com/frontweb/ffw/userComment_gw?',
        'Accept': 'application/json,text/plain,*/*',
        'Accept-Encoding': 'gzip,deflate,br,zstd'
    }

    return headers


def get_comments_total(cookies: str, comment_type: int):
    url = get_comments_query_url(cookies, comment_type)
    headers = get_comments_headers(cookies)

    res = requests.get(url=url, headers=headers)

    if res.status_code == 200:
        content = json.loads(res.text)
        if content['code'] == 0:
            return content['data']['total']
    return None


def filter_comments_fields(comment_type):
    def func(item):
        return {
            'comment_id': item['id'],
            'poi_id': item['wmPoiId'],
            'user_name': item['userName'],
            'content': item.get('comment', None),
            'order_details': json.dumps(item['orderDetails']),
            'comment_type': comment_type,
            'create_time': item['createTime']
        }

    return func


def get_comments(cookies: str, comment_type: int):
    total = get_comments_total(cookies, comment_type)

    if total is None:
        return False

    url = get_comments_query_url(cookies, comment_type, total)
    headers = get_comments_headers(cookies)

    res = requests.get(url=url, headers=headers)

    if res.status_code == 200:
        content = json.loads(res.text)
        if content['code'] == 0:
            comments = content['data']['list']
            ret = list(map(filter_comments_fields(comment_type), comments))

            for item in ret:
                c_model = CommentModel.objects.filter(comment_id=str(item['comment_id'])).first()
                if c_model is not None:
                    continue

                c = CommentModel(
                    comment_id=item['comment_id'],
                    poi_id=item['poi_id'],
                    user_name=item['user_name'],
                    content=item['content'],
                    order_details=item['order_details'],
                    comment_type=item['comment_type'],
                    create_time=item['create_time']
                )
                c.save()
            return True

    return False


if __name__ == '__main__':
    cookies = 'device_uuid=!83a9448e-7f9e-4d8d-ad73-50e95f27d752;uuid_update=true;shopCategory=food;JSESSIONID=h50rrtb3e6qv1ny6ynftof4;acctId=187417283;token=014A56OA2Z6LiViQqRQUWj1SRJ3mzzc-rckZQsR7thWE*;wmPoiId=20815629;isOfflineSelfOpen=0;city_id=310100;isChain=0;ignore_set_router_proxy=false;region_id=1000310100;region_version=1710840050;bsid=meNN-Gi_ZSt5ZinIOcE6Ss5ItfKkF29e_7rjk0eNs5yV3gYYsY6zzP26yi4YUSem24r1f3xireAxmQbcQwy3yw;city_location_id=310100;location_id=310113;has_not_waimai_poi=0;cityId=520200;provinceId=520000;set_info=%7B%22wmPoiId%22%3A%2220815629%22%2C%22region_id%22%3A%221000310100%22%2C%22region_version%22%3A1710840050%7D;wpush_server_url=wss://wpush.meituan.com;pushToken=014A56OA2Z6LiViQqRQUWj1SRJ3mzzc-rckZQsR7thWE*;setPrivacyTime=1_20240513;logan_session_token=jk94i3zb1p4di313qarv'
    get_comments(cookies, 1)
