import requests
import time
from datetime import datetime
import csv
import os

# https://weibo.com/ajax/statuses/buildComments
# is_reload=1
# id=5104159525179898
# is_show_bulletin=2
# is_mix=0&count=20
# type=feed
# uid=7895521166
# fetch_level=0
# locale=zh-CN

def init():
    if not os.path.exists('../Outcome/weiboDetail.csv'):
        with open('../Outcome/weiboDetail.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)
            #帖子id,作者名,作者头像,帖子标题,帖子内容,发帖地址，时间
            writer.writerow(['articleId',
                             'create_at',
                             'like_counts',
                             'region',
                             'content',
                             'authorName',
                             'authorGender',
                             'authorAddress',
                             'authorAvatar'])
def save_to_csv(resultData):
    with open('../Outcome/weiboDetail.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(resultData)

def get_All_ArticleList():#爬取所有标题
    articleList=[]
    with open('../Outcome/weibo.csv', 'r', encoding='utf-8') as file:
        readerCsv=csv.reader(file)
        next(file)#跳过第一行，因为第一行不是内容而是标题
        for nav in readerCsv:
            articleList.append(nav)
    return articleList

def get_data(url,params):
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.259.400 QQBrowser/12.6.5708.400',
        'cookie':'SINAGLOBAL=3343846262236.2007.1646141201339; SCF=Ajo4j-8ijO15-viUMbzUwUWdNVo2SrNBP5bc7AuHT9n79nkFV-xsffFqpumw8zArP_TqDBlKIZWQOSPdAtHJEpY.; XSRF-TOKEN=Ug1ysFgB7buhVABT6JlQCZPn; SUB=_2A25KQynzDeRhGeFP6VIX-CnFwj2IHXVpISM7rDV8PUNbmtANLVn_kW9NQTtuyxS8scNBOV2W7G_U3Z79Wz1cRBFP; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOM-3czELvlSTnIYwianou5NHD95QNeKz7SonN1K.pWs4Dqc_Ui--fiKy8i-2ci--4iK.Ni-2Ri--fi-zNi-2fi--fiK.fiKnci--Ri-88i-2pi--Ni-i2iK.peK.pi--NiKysi-82i--fiKLFi-2Ei--ciK.Xi-8si--4iKn0i-2R; ALF=02_1735321251; _s_tentry=weibo.com; Apache=99512397481.37386.1732729268165; ULV=1732729268169:4:1:1:99512397481.37386.1732729268165:1721996340648; WBPSESS=cndMrknLuyksZSbNi4GArC2Oa_1wb7eZnSk5N1AXFHZ7aNNWB4UAdQH6ABG9_JuaHna-SjWTZLrGupao7KZzKJPDjn4Zws9kkJ8Qj4FBjRQlmOuMiTybE_pcXqrl65WUw-hQRZslw8vGt7LMKWPbUQ=='
    }
    response=requests.get(url,headers=headers,params=params)
    if response.status_code==200:#200表示反应成功
        return response.json()['data']
    else:
        return None

def parse_json(response,articleId):
    for comment in response:
        articleId=articleId
        create_at=datetime.strptime(comment['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        like_counts=comment['like_counts']
        try:
            region = comment['source'].replace('来自','')
        except:
            region = '未知'
        content=comment['text_raw']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress= comment['user']['location']
        authorAvatar=comment['user']['avatar_large']
        print(articleId,create_at,like_counts,region,content,authorName,authorGender,authorAddress,authorAvatar)
        save_to_csv([articleId,create_at,like_counts,region,content,authorName,authorGender,authorAddress,authorAvatar])
        # break

def start_spider():
    commentUrl='https://weibo.com/ajax/statuses/buildComments'
    articleList= get_All_ArticleList()
    typeNumCount=0
    for article in articleList:
        articleId=article[0]
        print("正在获取帖子id为:%s的评论数据" % (articleId))
        time.sleep(2)
        params={
            'id':int(articleId),
            'is_show_bulletin':3
        }
        response=get_data(url=commentUrl,params=params)
        print(response)
        parse_json(response,articleId)
        # break

if __name__ == '__main__':
    init()
    start_spider()
