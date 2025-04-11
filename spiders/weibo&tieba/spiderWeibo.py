import requests
import time
from datetime import datetime
import csv
import os


def init():
    if not os.path.exists('../Outcome/weibo.csv'):
        with open('../Outcome/weibo.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)
            #帖子id,作者名,作者头像,帖子标题,帖子内容,发帖地址，时间
            writer.writerow(['aid',
                             'likeNum',
                             'commentsLen',
                             'reposts_count',
                             'region',
                             'content',
                             'contentLen',
                             'create_at',
                             'type',
                             'detailUrl',
                             'authorAvatar',
                             'authorName',
                             'authorDetail',
                             'isVip'])

def save_to_csv(resultData):
    with open('../Outcome/weibo.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(resultData)

def get_All_TypeList():#爬取所有标题
    typelist=[]
    with open('../Outcome/weiboNavData.csv', 'r', encoding='utf-8') as file:
        readerCsv=csv.reader(file)
        next(file)#跳过第一行，因为第一行不是内容而是标题
        for nav in readerCsv:
            typelist.append(nav)
    return typelist

def get_data(url,params):
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.259.400 QQBrowser/12.6.5708.400',
        'cookie':'SINAGLOBAL=3343846262236.2007.1646141201339; SCF=Ajo4j-8ijO15-viUMbzUwUWdNVo2SrNBP5bc7AuHT9n79nkFV-xsffFqpumw8zArP_TqDBlKIZWQOSPdAtHJEpY.; XSRF-TOKEN=Ug1ysFgB7buhVABT6JlQCZPn; SUB=_2A25KQynzDeRhGeFP6VIX-CnFwj2IHXVpISM7rDV8PUNbmtANLVn_kW9NQTtuyxS8scNBOV2W7G_U3Z79Wz1cRBFP; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFOM-3czELvlSTnIYwianou5NHD95QNeKz7SonN1K.pWs4Dqc_Ui--fiKy8i-2ci--4iK.Ni-2Ri--fi-zNi-2fi--fiK.fiKnci--Ri-88i-2pi--Ni-i2iK.peK.pi--NiKysi-82i--fiKLFi-2Ei--ciK.Xi-8si--4iKn0i-2R; ALF=02_1735321251; _s_tentry=weibo.com; Apache=99512397481.37386.1732729268165; ULV=1732729268169:4:1:1:99512397481.37386.1732729268165:1721996340648; WBPSESS=cndMrknLuyksZSbNi4GArC2Oa_1wb7eZnSk5N1AXFHZ7aNNWB4UAdQH6ABG9_JuaHna-SjWTZLrGupao7KZzKBSpP0zG5OQ0iB2v2pfRT6M25hAnI-zcsoFrTKZXhsVV4KY85SH0JKuzQxIek_VILA=='
    }
    response=requests.get(url,headers=headers,params=params)
    if response.status_code==200:#200表示反应成功
        return response.json()['statuses']
    else:
        return None

def parse_json(response,type):
    for article in response:
        aid=article['id']
        likeNum=article['attitudes_count']
        commentsLen = article['comments_count']
        reposts_count = article['reposts_count']
        try:
                region=article['region_name'].split()[1]
        except:
            if '发布于' in article['source'] :
                region =region=article['source'].split()[1]
            else:
                region='未知'
        content=article['text_raw']
        try:
            contentLen=article['textLength']
        except:
            contentLen=0
        create_at=datetime.strptime(article['created_at'], '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        type=type
        # 'https://weibo.com/5103520629918139/P1tAqFC9Z'
        try:
            detailUrl='https://weibo.com/'+str(article['id'])+'/'+str(article['mblogid'])
        except:
            detailUrl='无'
        authorAvatar=article['user']['avatar_large']
        authorName = article['user']['screen_name']
        authorDetail ='https://weibo.com/u/'+ str(article['user']['id'])
        isVip=article['user']['v_plus']
        # print(aid,likeNum,commentsLen,reposts_count,region,content,contentLen,create_at,type,detailUrl,authorAvatar,authorName,authorDetail,isVip)
        save_to_csv([aid,likeNum,commentsLen,reposts_count,region,content,contentLen,create_at,type,detailUrl,authorAvatar,authorName,authorDetail,isVip])


def start_spider(typeNum,pageNum):
    articleUrl='https://weibo.com/ajax/feed/hottimeline'
    typeList= get_All_TypeList()
    typeNumCount=0
    for type in typeList:
        if typeNumCount>typeNum:return#超过设定的爬取类型数就停下
        time.sleep(2)#加延迟以防被反爬
        for page in range(0,pageNum):
            print("正在获取的内容为: %s 频道的第%s页"%(type[0],page+1))
            time.sleep(1)
            params={
                'group_id':type[1],
                'containerid':type[2],
                'extparam':'discover|new_feed',
                'count':10
            }
            response=get_data(articleUrl,params)
            # print(response)
            parse_json(response,type[0])
            # break
        typeNumCount+=1
        # break

if __name__ == '__main__':
    init()
    typeNum=20       #要爬的导航栏频道数
    pageNum=3       #每个频道要爬的页数
    start_spider(typeNum, pageNum)
