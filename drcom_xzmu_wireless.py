#!/usr/bin/env python3
# author: fb0sh@outlook.com
# 配置你的信息
stu_number = "学号"
stu_passwd = "密码"

import re
import time
import json
import urllib
import requests

rq = requests.Session()

def get_login_config():
    try:
        respone= rq.get("http://10.1.0.213/", timeout=1)
    except:
        return {}

    redirect_url = set(re.findall('href="(.*?)"',respone.text)).pop()
    redirect_url = urllib.parse.unquote(redirect_url)
    if "?w" not in redirect_url: 
        return None

    print(f"[+] 🔗 登陆链接: {redirect_url}")

    config_args = urllib.parse.parse_qs(redirect_url)
    print(f"[+] ✌ 参数解析成功 ✅")

    return {
        'wlan_user_ip': config_args['wlanuserip'][0],
        'wlan_user_mac': config_args['http://10.1.0.212?wlanusermac'][0].replace('-',''),
        'wlan_ac_ip': config_args['wlanacip'][0],
        'wlan_ac_name': config_args['wlanacname'][0],
    }

def try_login():
    start_time = time.time()
    config = get_login_config()

    if len(config.keys()) == 0: # 已登陆
        return True

    if not config:
        return False


    login_url = "http://10.1.0.212:801/eportal/portal/login?callback=dr1003&login_method=1&terminal_type=1&lang=zh&lang=zh-cn&v=2833&jsVersion=4.2"\
        + f"&user_account=,0,{stu_number}"\
        + f"&user_password={stu_passwd}" \
        + f"&wlan_user_ip={config['wlan_user_ip']}&wlan_user_ipv6=" \
        + f"&wlan_user_mac={config['wlan_user_mac']}" \
        + f"&wlan_ac_ip={config['wlan_ac_ip']}" \
        + f"&wlan_ac_name={config['wlan_ac_name']}"

    response = rq.get(login_url)
    result = json.loads(re.findall("{.*?}",response.text).pop())

    # dr1003({'result': 0, 'msg': 'ldap auth error', 'ret_code': 1})
    # dr1003({'result': 1, 'msg': 'Portal协议认证成功！'})

    print(f"[*] 👀 响应信息: {result['msg']}")
    total = time.time() - start_time
    print(f"[*] ⌚ 共耗费 {total}秒")

    if result['result'] == 1:
        return True
    else:
        return False

if __name__ == "__main__":
    print("[*] Login 2 xzmu network (WIFI) [daemon] ver 1.0")

    while True:
        count = 0
        if try_login():
            print("[*] 💓 发送心跳包维持登陆状态")
            time.sleep(60*15)
        else:
            count += 1
            print(f"[*] 📚 正在重试 ({count})")
            time.sleep(30)
