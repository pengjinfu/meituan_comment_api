import json
import pprint

import requests


def get_orders_total(cookies, start_date, end_date, region_id):
    url = f'https://e.waimai.meituan.com/gw/api/order/mix/history/list/common?region_id={region_id}'
    headers = {
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    data = {
        'tag': 'complete',
        'startDate': start_date,
        'end_date': end_date,
        'pageNum': 1,
        'pageSIze': 10,
        'pageGray': 1
    }

    res = requests.post(url=url, headers=headers, data=data)

    if res.status_code == 200:
        content = json.loads(res.text)

        if content['code'] == 0:
            pprint.pprint(content['data']['totalCount'])
            return content['data']['totalCount']

    return None


def get_orders(cookies, start_date, end_date, region_id):
    total = get_orders_total(cookies, start_date, end_date, region_id)

    if total is None:
        return None

    pages = total // 10 + 1

    url = f'https://e.waimai.meituan.com/gw/api/order/mix/history/list/common?region_id={region_id}'
    headers = {
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    data = {
        'tag': 'complete',
        'startDate': start_date,
        'end_date': end_date,
        'pageNum': 1,
        'pageSize': 10,
        'pageGray': 1
    }

    orders = []
    for i in range(1, pages + 1):
        data.update({'pageNum': i})
        res = requests.post(url=url, headers=headers, data=data)
        if res.status_code == 200:
            content = json.loads(res.text)
            if content['code'] == 0:
                items = content['data']['wmOrderList']
                orders.extend(items)
    return orders


if __name__ == '__main__':
    region_id = '1000310100'
    cookies = 'device_uuid=!2bcf21b3-147d-4881-9e90-39ead5a1d553;uuid_update=true;shopCategory=food;JSESSIONID=blztmoyrtafn105aismmqnzbv;acctId=187417283;token=08jkxTxS2pq-j1enTRmGEzw0zyOoWVY9g0xnLbS7dJiA*;wmPoiId=20815629;isOfflineSelfOpen=0;city_id=310100;isChain=0;ignore_set_router_proxy=false;region_id=1000310100;region_version=1710840050;bsid=o27ljHlWG9x_Gf2KOoSJfYjIszEuvNXvPBiFAFMpgzFZpedDwTRqunCpohIwTwin_1r9DLw4yfp09yNurmLkIg;city_location_id=310100;location_id=310113;has_not_waimai_poi=0;cityId=310100;provinceId=310000;set_info=%7B%22wmPoiId%22%3A%2220815629%22%2C%22region_id%22%3A%221000310100%22%2C%22region_version%22%3A1710840050%7D;wpush_server_url=wss://wpush.meituan.com;pushToken=08jkxTxS2pq-j1enTRmGEzw0zyOoWVY9g0xnLbS7dJiA*;logan_session_token=t817lo51frv40x6dd26u;setPrivacyTime=1_20240513'
    start_date = '2024-05-08'
    end_date = '20240514'
    get_orders(cookies, start_date, end_date, region_id)
