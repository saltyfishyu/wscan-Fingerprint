#!/usr/bin/ python
# -*- coding:utf-8 -*-

import sys
import json
import requests
import re

requests.packages.urllib3.disable_warnings()


'''
-----ARL支持字段：-------
body = " "
title = ""
header = ""
icon_hash = ""
'''



def add_finger_origin(url, token):
    f = open("./finger.json",'r', encoding="utf-8")
    content =f.read()
    load_dict = json.loads(content)
        #dump_dict = json.dump(f)

    body = "body=\"{}\""
    title = "title=\"{}\""
    hash = "icon_hash=\"{}\""

    for i in load_dict['fingerprint']:
        finger_json =  json.loads(json.dumps(i))
        if finger_json['method'] == "keyword" and finger_json['location'] == "body":
            name = finger_json['cms']
            if len(finger_json['keyword']) > 0:
                for rule in finger_json['keyword']:
                    rule = body.format(rule)
                else:
                    rule = body.format(finger_json['keyword'][0])
                add_Finger(name, rule, url, token)

        elif finger_json['method'] == "keyword" and finger_json['location'] == "title":
            name = finger_json['cms']

            if len(finger_json['keyword']) > 0:
                for rule in finger_json['keyword']:
                    rule = title.format(rule)
                else:
                    rule = title.format(finger_json['keyword'][0])
                add_Finger(name, rule, url, token)
        else:
            name = finger_json['cms']
            if len(finger_json['keyword']) > 0:
                for rule in finger_json['keyword']:
                    rule = hash.format(rule)
                else:
                    rule = hash.format(finger_json['keyword'][0])
                add_Finger(name, rule, url, token)

'''
title_contains       标题中包含
body_contains        HTTP响应包中包含
protocol_contains    协议中包含
banner_contains      响应包中包含 包括HTTP以及TCP等
header_contains      HTTP响应头中包含
server_contains      HTTP响应头中Server值包含
cert_contains        证书包含
port_contains        端口包含
favicon_hash_is      网站图标ico的hash
''' 
def add_finger_wscan(url, token):
    f = open("../../wscan.json", "r", encoding="utf-8").read()
    content = json.loads(f)

    for item in content:
        product = item['product']
        condition = item['Condition']

        condition_parts = extract_conditions(condition)
        for part in condition_parts:
            if type(part) == list:
                part = part[0]

            body = "body=\"{}\""
            title = "title=\"{}\""
            hash = "icon_hash=\"{}\""
            header = "header=\"{}\""
            
            if "title_contains" in part:
                part = part.replace("title_contains(\"", "")
                part = part.replace("(", "")
                part = part.replace("\")", "")
                part = part.replace(")", "")
                title = title.format(part)
                add_Finger(product, title, url, token)
            
            if "body_contains" in part:
                part = part.replace("body_contains(\"", "")
                part = part.replace("(", "")
                part = part.replace("\")", "")
                part = part.replace(")", "")
                body = body.format(part)
                add_Finger(product, body, url, token)
            
            if "banner_contains" in part:
                part = part.replace("banner_contains(\"", "")
                part = part.replace("(", "")
                part = part.replace("\")", "")
                part = part.replace(")", "")
                header = header.format(part)
                add_Finger(product, header, url, token)
            
            if "header_contains" in part:
                part = part.replace("header_contains(\"", "")
                part = part.replace("(", "")
                part = part.replace("\")", "")
                part = part.replace(")", "")
                header = header.format(part)
                add_Finger(product, header, url, token)
            
            if "server_contains" in part:
                part = part.replace("server_contains(\"", "")
                part = part.replace("(", "")
                part = part.replace("\")", "")
                part = part.replace(")", "")
                header = header.format(part)
                add_Finger(product, header, url, token)
            
            if "favicon_hash_is" in part:
                part = part.replace("favicon_hash_is(\"", "")
                part = part.replace("(", "")
                part = part.replace("\")", "")
                part = part.replace(")", "")
                hash = hash.format(part)
                add_Finger(product, hash, url, token)

# 定义操作函数，用于提取值并与产品关联
def extract_conditions(condition):
    condition_parts = []
    if "&&" in condition:
        condition_splits = condition.split("&&")
        for split in condition_splits:
            split = split.strip()
            if len(extract_conditions(split)) > 1:
                condition_parts.extend(extract_conditions(split))
            else:
                condition_parts.append(extract_conditions(split))

    if "||" in condition:
        condition_splits = condition.split("||")
        for split in condition_splits:
            split = split.strip()
            if len(extract_conditions(split)) > 1:
                condition_parts.extend(extract_conditions(split))
            else:
                condition_parts.append(extract_conditions(split))
        
    if "&&" not in condition and "||" not in condition:
        condition_parts.append(condition)
    return condition_parts

def add_Finger(name, rule, url, token):
    headers = {
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
        "Connection": "close",
        "Token": "{}".format(token),
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Type": "application/json; charset=UTF-8"
    }
    url = "{}api/fingerprint/".format(url)
    data = {"name" : name,"human_rule": rule}
    data_json = json.dumps(data)

    try:
        response = requests.post(url, data=data_json, headers=headers, verify=False)
        if response.status_code == 200:
            print(''' Add: [\033[32;1m+\033[0m]  {}\n Rsp: [\033[32;1m+\033[0m] {}'''.format(data_json, response.text))
    except Exception as e:
        print(e)

def test(name,rule):

    return print("name: {}, rule: {}".format(name, rule))



if __name__ == '__main__':
    try:
        if 1 < len(sys.argv) < 5 :

            login_url = sys.argv[1]
            login_name = sys.argv[2]
            login_password = sys.argv[3]

            # login
            str_data = {"username": login_name, "password": login_password}
            login_data = json.dumps(str_data)
            if login_url[len(login_url)-1:] != "/":
                login_url = login_url + "/"
            login_res = requests.post(url="{}api/user/login".format(login_url), headers={
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
                "Content-Type": "application/json; charset=UTF-8"}, data=login_data, verify=False)

            # 判断是否登陆成功：
            # print(login_res.text)
            if "401" not in login_res.text:

                #print(type(login_res.text))
                token = json.loads(login_res.text)['data']['token']
                print("[+] Login Success!!")

                # old
                # add_finger_origin(login_url, token)
                # main
                add_finger_wscan(login_url, token)
            else:
                print("[-] login Failure! ")
        else:
            print('''
    usage:

        python3 ARl-Finger-ADD.py https://192.168.1.1:5003/ admin password

                                                         modify by yuf1sher
            ''')
    except Exception as a:
        print(a)