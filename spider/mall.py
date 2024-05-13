import json
import requests
import config.spider


def get_mall_info(cookies):
    headers = {
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    res = requests.get(config.spider.MALL_INFO_API_URL, headers=headers)

    if res.status_code == 200:
        res_content = json.loads(res.text)

        if res_content['code'] == 0:
            poi_name = res_content['data']['wmPoiName']
            return poi_name

    return None


def get_mall_huifulv(cookies):
    headers = {
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    url = 'https://e.waimai.meituan.com/gw/api/im/rights/v2/top/tips?region_id=1000310100&region_version=1710840050&yodaReady=h5&csecplatform=4&csecversion=2.4.0'

    data = {
        'wmPoiId': '20815629'
    }

    res = requests.post(url=url, headers=headers, data=data)

    if res.status_code == 200:
        content = json.loads(res.text)
        if content['code'] == 0:
            ret = content['data']['title']
            print(ret)
            return ret
    return None


if __name__ == '__main__':
    cookies = 'device_uuid=!83a9448e-7f9e-4d8d-ad73-50e95f27d752;uuid_update=true;shopCategory=food;JSESSIONID=h50rrtb3e6qv1ny6ynftof4;acctId=187417283;token=014A56OA2Z6LiViQqRQUWj1SRJ3mzzc-rckZQsR7thWE*;wmPoiId=20815629;isOfflineSelfOpen=0;city_id=310100;isChain=0;ignore_set_router_proxy=false;region_id=1000310100;region_version=1710840050;bsid=meNN-Gi_ZSt5ZinIOcE6Ss5ItfKkF29e_7rjk0eNs5yV3gYYsY6zzP26yi4YUSem24r1f3xireAxmQbcQwy3yw;city_location_id=310100;location_id=310113;has_not_waimai_poi=0;cityId=520200;provinceId=520000;set_info=%7B%22wmPoiId%22%3A%2220815629%22%2C%22region_id%22%3A%221000310100%22%2C%22region_version%22%3A1710840050%7D;wpush_server_url=wss://wpush.meituan.com;pushToken=014A56OA2Z6LiViQqRQUWj1SRJ3mzzc-rckZQsR7thWE*;setPrivacyTime=1_20240513;logan_session_token=jk94i3zb1p4di313qarv'
    get_mall_huifulv(cookies)