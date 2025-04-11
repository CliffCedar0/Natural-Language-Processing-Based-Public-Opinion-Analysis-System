
url=('https://tieba.baidu.com/mg/f/getFrsData?kw=抗压背锅=10&pn=1'
 '&is_good=0&cid=0&sort_type=0&fr=&default_pro=1&only_thread_list=0&eqid=&refer=tieba.baidu.com')
import requests
import datetime
import csv
import os

class spider(object):
    def __init__(self,areaName):
        self.areaName = areaName
        self.spiderUrl=('https://tieba.baidu.com/mg/f/getFrsData?rn=10'
                        '&is_good=0'
                        '&cid=0'
                        '&sort_type=0'
                        '&fr='
                        '&default_pro=1'
                        '&only_thread_list=0'
                        '&eqid=&refer=tieba.baidu.com')
        self.headers={
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) '
                         'AppleWebKit/605.1.15 (KHTML, like Gecko) '
                         'Version/13.0.3 '
                         'Mobile/15E148 Safari/604.1'
        }
    #存储地
    def init(self):
        if not os.path.exists('../Outcome/tieba.csv'):
            with open('../Outcome/tieba.csv', 'a', newline='', encoding='utf-8') as wf:
                writer=csv.writer(wf)
                writer.writerow(["area","tid","author","authorImg","title","content","likeNum","replyNum","postTime"])
    def save_to_csv(self,resultData):
        with open('../Outcome/tieba.csv', 'a', newline='', encoding='utf-8') as f:
            writer=csv.writer(f)
            writer.writerow(resultData)

    def main(self,page):
        params={
            'pn':int(page),
            'kw':self.areaName
        }
        pageJson=requests.get(self.spiderUrl,headers=self.headers,params=params).json()
        pageJson=pageJson["data"]["thread_list"]
        # print(pageJson)
        for index,card in enumerate(pageJson):
            area=self.areaName#吧名
            tid=card['tid']#帖子id
            author=card['author']['name']#作者名
            authorImg=('https://gss0.bdstatic.com/6LZ1dD3d1sgCo2Kml5_Y_D3/sys/portrait/item/'
                       + card['author']['portrait'])#作者头像
            title=card['title']#标题
            content=card['abstract'][0]['text']
            try:#点赞数
                likeNum=card['agree']['agree_num']
            except:
                likeNum=0

            try:#回复量
                replyNum=card['reply_num']
            except:
                replyNum=0

            try:#发布时间
                postTime=card['create_time']
                postTime=datetime.datetime.fromtimestamp(postTime)#时间戳转换为正常时间
            except:
                postTime=card['last_time_int']
                postTime=datetime.datetime.fromtimestamp(postTime)
            # print(area,author,authorImg,title,content,likeNum,replyNum,postTime)
            self.save_to_csv([area,tid,author,authorImg,title,content,likeNum,replyNum,postTime])
            # break

if __name__ == '__main__':
    arealist=['抗压背锅','天堂鸡汤','第五人格','原神内鬼','羽毛球','新闻']
    # spiderObj=spider('抗压背锅')
    # spiderObj.init()
    for area in arealist:
        spiderObj=spider(area)
        spiderObj.init()
        for page in range(1,6):
            spiderObj.main(page)
        # break