import csv
import datetime
import os
import time
import requests
import numpy as np
import json


def save_to_csv(resultData):
    with open('结果/navData.csv', 'a', newline ='', encoding='utf-8') as wf:
        writer = csv.writer(wf)#
        writer.writerow(resultData)#写入数据
        print("写入数据")

def init(self):
    if not os.path.exists('结果/navData.csv'):  # 判断文件是否存在
        with open('结果/navData.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)  # 写入表头
            print("写入表头")
            writer.writerow(["typeName", "gid", "containerid"])
            #
            print("文件创建成功")
    else:
        print("文件已存在")

def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'cookie':'SCF=AryeBeMawiC3YM1mnPJRAdR9KAFcZrT6tKVXlvcTePuydHmshKRQVVw-VIw_XUFkmGYBeHS_D5FZd2e8WS5-Uq8.; XSRF-TOKEN=3g1zkkb_cUeFlzgc48pd0lY1; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5PiwnjJ2PvMV53L248EaXP5JpVF02Re0-4eoBpeKn4; SUB=_2AkMQcn_6dcPxrAVSn_wVyG_hboRH-jyjpxYMAn7uJhMyAxh37mgDqSVutBF-XHeUchcvon1uFkq1vYBWIKTz7I1t; WBPSESS=Dt2hbAUaXfkVprjyrAZT_CtdSRKgctHTYVay9uSpEFzq5aNPoN2980CKJjLt78xqnv3obKnZSqpaetH-I8fw7QSH1bx4jHQK1DQz6pIVVWbHB9Cq7JD3Fci_yL9eS9SEy5kXxsa3cZpUOYLuJusHxw=='
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        save_to_csv([navName,gid,containerid])


if __name__ == '__main__':
    #init()
    url = 'https://weibo.com/ajax/feed/allGroups?is_new_segment=1&fetch_hot=1'
    response = get_data(url)
    parse_json(response)