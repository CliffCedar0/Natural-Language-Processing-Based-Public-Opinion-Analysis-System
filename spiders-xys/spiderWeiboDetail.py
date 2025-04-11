import time
import requests
import csv
import os
from datetime import datetime

def init():
    if not os.path.exists('结果/weiboDetail.csv'):  # 判断文件是否存在
        with open('结果/weiboDetail.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)  # 写入表头
            print("写入表头")
            writer.writerow(
                ["articleId",
                "created_at",
                "likes_counts",
                "region",
                "content",
                "authorName",
                "authorGender",
                "authorAddress",
                "authorAvatar",
            ])
            #
            print("文件创建成功")
    else:
        print("文件已存在")

def save_to_csv(resultData):
    with open('结果/weiboDetail.csv', 'a', newline ='', encoding='utf-8') as wf:
        writer = csv.writer(wf)#
        writer.writerow(resultData)#写入数据
        print("写入数据")


def getdata(url,params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'cookie': 'SCF=AryeBeMawiC3YM1mnPJRAdR9KAFcZrT6tKVXlvcTePuydHmshKRQVVw-VIw_XUFkmGYBeHS_D5FZd2e8WS5-Uq8.; SINAGLOBAL=2194215254634.737.1731132648527; ULV=1731136587912:2:2:2:6791253986608.477.1731136587910:1731132648588; XSRF-TOKEN=YdDED3AOhZNWut5GcptNX1Qo; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5PiwnjJ2PvMV53L248EaXP5JpVF02Re0-4eoBpeKn4; SUB=_2AkMQZQPtdcPxrAVSn_wVyG_hboRH-jyjsGobAn7uJhMyAxh37g4MqSVutBF-XEdP6FDRnjsEdkSvJ1u7-HZDnfZG; WBPSESS=Dt2hbAUaXfkVprjyrAZT_CtdSRKgctHTYVay9uSpEFzq5aNPoN2980CKJjLt78xqnv3obKnZSqpaetH-I8fw7em9MW2kuUey-8e7sDQ2CJMzL9aUs_S0gwad-mx8D71Fm5I7l3G_0vfooNDIbNfRQQ=='
    }

    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None


def getAllArticleList():
    articleList = []
    with open('结果/weibo.csv', 'r', encoding='utf-8') as reader:
        readerCsv= csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            articleList.append(nav)
    return articleList


def pase_json(response,acticleId):
    for comment in response:
        acticleId = acticleId
        created_at = datetime.strptime(comment['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        likes_counts = comment['like_counts']
        try:
            region = comment['source'].replace('来自','')
        except:
            region = '无'
        content = comment['text_raw']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location']
        authorAvatar = comment['user']['avatar_large']


        save_to_csv([acticleId,created_at,likes_counts,region,content,authorName,authorGender,authorAddress,authorAvatar])




def start():
    commentUrl = 'https://weibo.com/ajax/statuses/buildComments'
    articleList = getAllArticleList()
    typeNumCount = 0
    for article in articleList[1:]:
        articleId = article[0]
        print('正在爬取id为%s的评论数据'%articleId)
        time.sleep(2)
        params = {
            'id':int(articleId),
            'is_show_bulletin': 3,
        }
        response = getdata(commentUrl,params)
        pase_json(response,articleId)

if __name__ == '__main__':
    #init()  # 确保每次运行都是从干净的状态开始
    start()
