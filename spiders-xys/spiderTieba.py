import csv
import datetime
import os
import time
import pytz  # 如果需要自定义时区
import django
import requests
import pandas as pd
# 设置 Django 配置文件路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '微博舆情分析.settings')
django.setup()

# 导入 Django 模块
from myApp.models import TiebaInfo
from django.utils.timezone import make_aware

class Spider(object):
    def __init__(self, areaName, page):
        self.areaName = areaName  # 贴吧名称
        self.page = page  # 页数
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36 Edg/129.0.0.0'
        }
        self.spiderUrl = 'https://tieba.baidu.com/mg/f/getFrsData?kw=%s&rn=100&pn=%s&is_good=0&cid=0&sort_type=0&fr=&default_pro=1&only_thread_list=0&eqid=&refer=tieba.baidu.com'

    def main(self, page):
        params = {
            'pn': page,
            'kw': self.areaName,
        }
        try:
            print('这个是链接:\n' + self.spiderUrl % (self.areaName, page))
            print()
            response = requests.get(self.spiderUrl % (self.areaName, page), headers=self.headers, params=params)
            response.raise_for_status()  # 检查请求是否成功

            if response.status_code == 200:
                try:
                    pageJson = response.json()
                    pageJson = pageJson['data']['thread_list']
                    #print(pageJson)
                except requests.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Response text: {response.text}")
            else:
                print(f"Unexpected status code: {response.status_code}")
                print(f"Response text: {response.text}")
        except requests.RequestException as e:
            print(f"请求出错: {e}")

        for index,card in enumerate(pageJson):
            tiebaData = []
            area = self.areaName
            tid = card['tid']
            try:
                author = card['author']['name']
            except:
                author = '匿名用户'
            authorImg = 'https://gss0.bdstatic.com/6LZ1dD3d1sgCo2Kml5_Y_D3/sys/portrait/item/' + card['author']['portrait']
            title = card['title']
            content = card['abstract'][0]['text'] if 'abstract' in card and card['abstract'] else ''
            try:
                likeNum = card['agree']['agree_num']
            except:
                likeNum = 0
            replyNum = card['reply_num']
            try:
                postTime = card['create_time']
                postTime = datetime.datetime.fromtimestamp(postTime)
            except:
                postTime = card['last_time_int']
                postTime = datetime.datetime.fromtimestamp(postTime)
            tiebaData.append(area)
            tiebaData.append(tid)
            tiebaData.append(author)
            tiebaData.append(authorImg)
            tiebaData.append(title)
            tiebaData.append(content)
            tiebaData.append(likeNum)
            tiebaData.append(replyNum)
            tiebaData.append(postTime)
            tiebaData.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.save_to_csv(tiebaData)
            print(tiebaData)



    def save_to_csv(self,rowData):
        with open('结果/tieba.csv', 'a', newline ='', encoding='utf-8') as wf:
            writer = csv.writer(wf)#
            writer.writerow(rowData)#写入数据
            print("写入数据")

    def clear_csv(self):
        df = pd.read_csv('结果/tieba.csv')
        df.drop_duplicates(inplace=True)
        print("总数据为%d" % df.shape[0])
        return df.values


    def save_to_sql(self):
        data = self.clear_csv()
        for row in data:
            TiebaInfo.objects.create(
                area = row[0],
                tid = row[1],
                author = row[2],
                authorImg = row[3],
                title = row[4],
                content = row[5],
                likeNum = row[6],
                replyNum = row[7],
                postTime = row[8],
                createTime = row[9]
            )




    def init(self):
        if not os.path.exists('结果/tieba.csv'):  # 判断文件是否存在
            with open('结果/tieba.csv', 'a', newline='', encoding='utf-8') as wf:
                writer = csv.writer(wf)  # 写入表头
                print("写入表头")
                writer.writerow(["area", "tid", "author", "authorImg", "title", "content", "likeNum", "replyNum", "postTime"])
                #关键词，贴吧ID，作者名，作者头像，标题，内容，点赞数，收藏数，回复时间
                print("文件创建成功")
        else:
            print("文件已存在")


if __name__ == '__main__':  # 测试



    # areaList=['地狱笑话','孙笑川'] #需要爬取的贴吧名称
    # for area in areaList:
    #     spiderObj = Spider(area, 1)
    #     for page in range(1,20):  #循环X次，一次返回十段数据，因为你链接里rn=10
    #         spiderObj.main(page)
    #         time.sleep(1)  # 防止请求过快被封禁


    spiderObj = Spider('天堂鸡汤', 1)
    spiderObj.init()
    spiderObj.save_to_sql()  # 保存到数据库
