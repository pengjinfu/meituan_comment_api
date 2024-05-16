import json
import requests

import config.common
import tools


def get_mall_info(cookie):
    url = 'https://e.waimai.meituan.com/api/v2/account/homePage'
    headers = {
        'Cookie': cookie,
        'User-Agent': config.common.USER_AGENT
    }
    res = requests.get(url=url, headers=headers)

    if res.status_code == 200:
        content = json.loads(res.text)
        if content['code'] == 0:
            mall_info = content['data']
            return mall_info

    return None


def get_mall_hui_fu_lv(cookie):
    cookie_dict = tools.cookies2dict(cookie)
    mall_info = get_mall_info(cookie)
    url = f'https://e.waimai.meituan.com/gw/api/im/rights/v2/top/tips?region_id={mall_info["regionId"]}'
    headers = {
        'Cookie': cookie,
        'User-Agent': config.common.USER_AGENT
    }

    data = {
        'wmPoiId': cookie_dict['wmPoiId']
    }

    res = requests.post(url=url, headers=headers, data=data)

    if res.status_code == 200:
        content = json.loads(res.text)
        if content['code'] == 0:
            hui_fu_lv = content['data']['title']
            return hui_fu_lv

    return None
