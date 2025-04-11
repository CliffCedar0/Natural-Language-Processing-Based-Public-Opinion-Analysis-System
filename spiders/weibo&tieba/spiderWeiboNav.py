import requests
import csv
import numpy as np
import os

def init():
    if not os.path.exists('../Outcome/weiboNavData.csv'):
        with open('../Outcome/weiboNavData.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)
            writer.writerow(["typeName", "gid", "containerid"])

def save_to_csv(resultData):
    with open('../Outcome/weiboNavData.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(resultData)

def get_data(url):
    headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.259.400 QQBrowser/12.6.5708.400",
        "cookie":"SINAGLOBAL=3343846262236.2007.1646141201339; SCF=Ajo4j-8ijO15-viUMbzUwUWdNVo2SrNBP5bc7AuHT9n79nkFV-xsffFqpumw8zArP_TqDBlKIZWQOSPdAtHJEpY.; XSRF-TOKEN=Ug1ysFgB7buhVABT6JlQCZPn; SUB=_2A25KQynzDeRhGeFP6VIX-CnFwj2IHXVpISM7rDV8PUNbmtANLVn_kW9NQTtuyxS8scNBOV2W7G_U3Z79Wz1cRBFP; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOM-3czELvlSTnIYwianou5NHD95QNeKz7SonN1K.pWs4Dqc_Ui--fiKy8i-2ci--4iK.Ni-2Ri--fi-zNi-2fi--fiK.fiKnci--Ri-88i-2pi--Ni-i2iK.peK.pi--NiKysi-82i--fiKLFi-2Ei--ciK.Xi-8si--4iKn0i-2R; ALF=02_1735321251; WBPSESS=cndMrknLuyksZSbNi4GArC2Oa_1wb7eZnSk5N1AXFHZpAAggIhY5IhX5trf5HILeYIWbDapnAbiuFwmh_2uPGKn6p16W2-GrmR_6zGCUqwlqz9VIMHomM2LLlj2gZPGOE0hYl12UWZg8e_T_STMgiA==; _s_tentry=weibo.com; Apache=99512397481.37386.1732729268165; ULV=1732729268169:4:1:1:99512397481.37386.1732729268165:1721996340648"
    }
    response = requests.get(url,headers=headers)
    if response.status_code==200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList=np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        navName=nav['title']
        gid=nav['gid']
        containerid=nav['containerid']
        save_to_csv([navName,gid,containerid])

if __name__ == '__main__':
    init()
    url="https://weibo.com/ajax/feed/allGroups?is_new_segment=1&fetch_hot=1"
    response = get_data(url)
    parse_json(response)

