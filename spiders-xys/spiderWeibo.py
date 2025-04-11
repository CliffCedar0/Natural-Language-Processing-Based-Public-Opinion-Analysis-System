import time
import requests
import csv
import os
from datetime import datetime



def init():
    if not os.path.exists('结果/weibo.csv'):  # 判断文件是否存在
        with open('结果/weibo.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)  # 写入表头
            print("写入表头")
            writer.writerow(
                ["aid",
                "likeNum",
                "commentsLen",
                "reposts_count",
                "region",
                "content",
                "contentLen",
                "created_at",
                "type",
                "detailUrl",
                "authorAvater",
                "authorName",
                "authorDetail",
                "isVip"])
            #
            print("文件创建成功")
    else:
        print("文件已存在")

def save_to_csv(resultData):
    with open('结果/weibo.csv', 'a', newline ='', encoding='utf-8') as wf:
        writer = csv.writer(wf,quoting=csv.QUOTE_NONNUMERIC, quotechar='"')
        writer.writerow(resultData)#写入数据
        print("写入数据")


def getdata(url,params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        'cookie': 'SCF=AryeBeMawiC3YM1mnPJRAdR9KAFcZrT6tKVXlvcTePuydHmshKRQVVw-VIw_XUFkmGYBeHS_D5FZd2e8WS5-Uq8.; SINAGLOBAL=2194215254634.737.1731132648527; ULV=1731136587912:2:2:2:6791253986608.477.1731136587910:1731132648588; XSRF-TOKEN=YdDED3AOhZNWut5GcptNX1Qo; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9W5PiwnjJ2PvMV53L248EaXP5JpVF02Re0-4eoBpeKn4; SUB=_2AkMQZQPtdcPxrAVSn_wVyG_hboRH-jyjsGobAn7uJhMyAxh37g4MqSVutBF-XEdP6FDRnjsEdkSvJ1u7-HZDnfZG; WBPSESS=Dt2hbAUaXfkVprjyrAZT_CtdSRKgctHTYVay9uSpEFzq5aNPoN2980CKJjLt78xqnv3obKnZSqpaetH-I8fw7em9MW2kuUey-8e7sDQ2CJMzL9aUs_S0gwad-mx8D71Fm5I7l3G_0vfooNDIbNfRQQ=='
    }

    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()['statuses']
    else:
        return None


def getAllTypeList():
    typeList = []
    with open('结果/navData.csv', 'r', encoding='utf-8') as reader:
        readerCsv= csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            typeList.append(nav)
    return typeList


def pase_json(response,type):
    for article in response:
        aid = article['id']
        likeNum = article['attitudes_count']
        commentsLen = article['comments_count']
        reposts_count = article['reposts_count']
        try:
            region = article['region_name'].replace('发布于','')
        except:
            region = '无'
        content = article['text_raw']
        try:
            contentLen = article['textLength']
        except:
            contentLen = '无'
        create_at = datetime.strptime(article['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        type = type
        try:
            detailUrl = 'https://weibo.com/' + str(article['id']) + '/' + str(article['mblogid'])
        except:
            detailUrl = '无'
        authorAvatar = article['user']['avatar_large']
        authorName = article['user']['screen_name']
        authorDetail = 'https://weibo.com/' + str(article['user']['id'])
        isVip = article['user']['v_plus']
        print(detailUrl)
        save_to_csv([aid,likeNum,commentsLen,reposts_count,region,content,contentLen,create_at,type,detailUrl,authorAvatar,authorName,authorDetail,isVip])

def start(typeNum=120,pageNum=10):  #爬取什么类型，爬多少页
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    typeList = getAllTypeList()
    typeNumCount = 0
    for type in typeList:
        if typeNumCount > typeNum:return
        time.sleep(2)
        for page in range(0,pageNum):
            print("正在爬取的类型：%s中第%s页的数据"%(type[0],page +1))
            time.sleep(1)
            params = {
                'group_id': type[1],
                'containerid': type[2],
                'extparam': "discover|new_feed",
                'max_id': page,
                'count': 10,
            }
            response = getdata(articleUrl,params)
            pase_json(response,type[0])
        typeNumCount += 1


if __name__ == '__main__':
    #init()  # 确保每次运行都是从干净的状态开始
    start()
