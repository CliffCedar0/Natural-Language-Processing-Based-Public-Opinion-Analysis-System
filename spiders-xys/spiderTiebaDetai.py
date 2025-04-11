import os
import csv
import time
import json
import datetime
import django
import requests
import traceback
import pandas as pd
from lxml import etree

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '微博舆情分析.settings')
django.setup()


from myApp.models import TiebaDetailInfo


page_count = 2

#标头一定得对，不然无法爬取
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'cookie':'NO_UNAME=1; baidu_broswer_setup_=0; XFI=44c8d940-a7fe-11ef-a11c-eb4b6f6b64ff; XFCS=83262017E4AB62D0596D93D2BCB4F6F28284A45A8F47B22183B7FB3B1A23EF5A; XFT=7qiMPALkedssvaX0CU0xSLts8siucjPxHz39PW1lLbk=; IS_NEW_USER=251e382d49ccaa1a8e036c23; BAIDUID=DDE259A713AF68AF5DFA6E7DF0588E34:FG=1; BAIDUID_BFESS=DDE259A713AF68AF5DFA6E7DF0588E34:FG=1; BAIDU_WISE_UID=wapp_1732168420891_367; ZFY=UUFEDfIZtedMQxcVeT133P9:AiNkJFs9H0RyeDDkgwhA:C; arialoadData=false; wise_device=0; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1732174059,1732174228,1732176038,1732189554; HMACCOUNT=66699663461F7B5F; USER_JUMP=-1; st_key_id=17; ppfuid=FOCoIC3q5fKa8fgJnwzbE67EJ49BGJeplOzf+4l4EOvDuu2RXBRv6R3A1AZMa49I27C0gDDLrJyxcIIeAeEhD8JYsoLTpBiaCXhLqvzbzmvy3SeAW17tKgNq/Xx+RgOdb8TWCFe62MVrDTY6lMf2GrfqL8c87KLF2qFER3obJGnxB/OzeZl1L8WWDqLeeVrPGEimjy3MrXEpSuItnI4KD8kj6srEFNxlzHu5N6Z0HBkHX7NaKxobB9tVxIqVWE9NUjh+QmF6BN2lLnbZ95zo47s62M3E4Hl4fhdTcuzql8EUzhzJZqcLOqkaHsCtaEmnNb9osI9d3WjPvWlieRiQkLv0lGxeY1eQFMs/4wYiIClTm2gwh4FiWR92a0xmB5ou1yQfc98tqPCqsXqeVwQrLhQHaIsA/c4dW9jCybDTmXGOt76hIOwIkl8Cknhh5VLurBlf6NStoa2n2bwW5bo3tZ7zVyBFtqcI+AVyDUjRazzKBFSftpHIF5AhAJheUhCvBTG+/iRVsTRqANCTYr+oQm9IJF6ZBKSEourVR4fobEIn4wAhhs9DGyyPQALrb0DZi6L0BPA661JDj0lmZIgcCFL8aJ0hktpYIjWQcYCvzWnej97H78r2IclzcMZuksx/jo2tZenMvbqD+8uOOiC2tQixDmldYw5BqJLDYUbZ+wfNQnppLrHYBEemmlFd+EeHhlok1JQqnW3/KBh2HKJm1mF+UcHg6krT8DM3UvAE++soFYr+5ZxeMa2JIYEijZTEMD5D/OhnyGxgqrhgDmyXws4zhn9mYeB1wThtZ/TdEKwc71CijYOWBU1idVaHcH9y2XVhb4w8S4/frnYI6IYLuS2u3pTzUllPaUj8GpkCVC31ZXXZco39g0jXRWpLHNOGoj1Mx3RpDpK5PT8HNXbZwtRdpo4vxfVUN+bZNqoaRXo1fyFSZ8DszVTrZzNsgyy8jru3MhLDk8CW9ov/nYSeLr4aPyLkg7Gk359g98BIGN/ZzJR/h+Y6AyFx+HlMoYJnS06dVmqFbvlCtSdGylKQ5f8eWtxPkJGqOFtWjIVteQYMsH/AaSJonqw+WLiZvGjYfm9p0alEyujapoTy77HzDcUoU1wUSXa5xS/Z6hXEr2OnLi0LdPVcGjz8lpLcdVeSoS0dzyQBCDKd+z9/bz/dM9VllC1+aCCc8K28RWpYmU0S24R9DDZVx3j3+tLLpw3BYd+viGvOL2+4B+aikqOb5pyJ37/Fv6yLTnzQ26RApvxiFA4Xm0FwKInrF/bb/ee9ppq0gKweencPxgS/jd0rjw==; BDUSS=EY5aUx5a0g1bEc3ZVUwbUExbWswc3V6MGg0aE5EbXlFOVVzQVJGSTFoNmNxbVpuSVFBQUFBJCQAAAAAAAAAAAEAAACodfZ55b6Q6I-y6I-y4pmhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwdP2ecHT9nR; BDUSS_BFESS=EY5aUx5a0g1bEc3ZVUwbUExbWswc3V6MGg0aE5EbXlFOVVzQVJGSTFoNmNxbVpuSVFBQUFBJCQAAAAAAAAAAAEAAACodfZ55b6Q6I-y6I-y4pmhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJwdP2ecHT9nR; STOKEN=0fe17193be64784821057d6964a9b22fb90e94dceab845a3e40b2f517ee823b3; BA_HECTOR=2k21200ga02k0l2h2hahag8422qjn71jju7cv1v; ab_sr=1.0.1_YTk0OTI2NDUzOTUwODhjMDQzMzU3MWJlMTA3ZGIzOTdmY2M2YmQ0NTQ1MWVlOWRiMzcwMGI1MWEyNjMyMTNmMDUyZjRkOTUxYzM0ZTJlNGY1MTAzMGE3OGU1YTQwNjk4Y2YxNjBjNmM1YTM3ODRjNjRiYzY5ZjM5NThiMGY2ZjQyNDMzODM2NDBhZDEzZDRmNGQyOTJkNTYxYjc5ZDA0ODBkMDU3MDYzYzkwNjQ0Y2NkMjAxOTZkMWQxY2UyNTRl; st_data=564556cb7799853be34af9d3b5ba65fad942dca2a8d3922965630ed788e30e063a1748d8287d18d3ba919921456357f590d3d5d45e644665b8c04906658adccdcb64d716c6939e41a74ada4228e66712137d4e012006642949c046796fad6c414d841caf4d60d8fc7a5f680a7f2e5216269aef22fc871e1a9746cc05fa66228669c0a710ed5dbd6cda45240a1f53ad89; st_sign=8dd46474; tb_as_data=6aed1ad08efbef0ae5c9f9dce2f1b7f2460474ca78fffd498f670c8b146d4186347e0d6bdf43160bb5334dc3fdd1ee724d87b93964a73cc17089b6b89a4e570cff428d2fe41073b3e19f0248c4d1036699a1b5b94507021cfdcb84673bb907a00c1c1b63464119c0b19e8470d07b0b48; RT="z=1&dm=baidu.com&si=e42fc7af-f158-4837-a89f-5a86fd5f3a24&ss=m3r8xoov&sl=8&tt=yyh&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=11vr&ul=18ta&hd=1ahk"; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1732189613'
} #请求头(里面要包含你自己当前的cookie和User-Agent,如果要更新)


def spider_out(tid, page):
    global page_count
    detailUrl = f'https://tieba.baidu.com/p/{tid}?pn={page}'
    print('详情页面:' + detailUrl)
    response = requests.get(detailUrl, headers=headers, timeout=60).text  #response返回的是一整个静态页面
    page_tree = etree.HTML(response)
    div_list = page_tree.xpath('//div[@id="j_p_postlist"]/div')


    if page == 1:
        div_list = div_list[1:]  # 排除第一个元素

    for index, divC in enumerate(div_list):
        tiebaDetailData = []
        print("正在爬取帖子id：%d的页面第%d条数据" % (tid,index + 1))
        tid = tid
        # 获取作者名称并进行检查
        comAuthorList = divC.xpath('.//li[@class = "d_name"]/a/text()')
        if comAuthorList:
            comAuthor = comAuthorList[0]
        else:
            comAuthor = "未知作者"  # 设置一个默认值


        comAuthorImgList = divC.xpath('.//div[@class="icon_relative j_user_card"]/@data-field')

        if comAuthorImgList:
            comAuthorImg = comAuthorImgList[0]
            try:
                imgData = json.loads(comAuthorImg)
                comAuthorImg = imgData['id']
                comAuthorImg = 'https://gss0.bdstatic.com/6LZ1dD3d1sgCo2Kml5_Y_D3/sys/portrait/item/' + comAuthorImg
            except json.JSONDecodeError:
                print("JSON解析错误，comAuthorImg内容可能不是有效的JSON格式")
                comAuthorImg = "无头像"  # 或者设置为默认值，或者留空
        else:
            comAuthorImg = "无头像"  # 或者设置为默认值，或者留空
        # 这里可以添加其他数据的提取逻辑，并进行相同的空值检查
        # 例如，提取评论内容
        comContent = divC.xpath('.//div[@class="post_bubble_middle_inner"]/text()')
        comContent = ''.join(comContent)
        if comContent == '':
            comContent = divC.xpath('.//div[@class="d_post_content j_d_post_content "]/text()')
            comContent = ''.join(comContent)
        else:
            comContent = comContent

        comAddressList = divC.xpath('.//div[@class="post-tail-wrap"]/span[1]/text()')
        if comAddressList:
            comAddress = comAddressList[0].split(':')[1]  # 确保列表不为空后再操作
        else:
            comAddress = "地址信息缺失"  # 如果没有找到地址信息，设置默认值

        try:
            comTime = divC.xpath('.//div[@class="post-tail-wrap"]/span[5]/text()')[0]
            if "楼" in comTime:
                comTime = divC.xpath('.//div[@class="post-tail-wrap"]/span[6]/text()')[0]
        except:
            comTime = "时间信息缺失"  # 如果没有找到时间信息，设置默认值

        # 输出提取到的内容
        tiebaDetailData.append(tid)
        tiebaDetailData.append(comAuthor)
        tiebaDetailData.append(comAuthorImg)
        tiebaDetailData.append(comContent)
        tiebaDetailData.append(comAddress)
        tiebaDetailData.append(comTime)

        save_to_csv(tiebaDetailData)


def save_to_csv(rowData):
    with open('结果/tiebaDetail.csv', 'a', newline ='', encoding='utf-8') as wf:
        writer = csv.writer(wf)#
        writer.writerow(rowData)#写入数据
        print("写入数据")


def clear_csv(self):
    df = pd.read_csv('结果/tiebaDetail.csv')
    df.drop_duplicates(inplace=True)
    print("总数据为%d" % df.shape[0])
    return df.values

def save_to_sql(self):
    data = self.clear_csv()
    for job in data:
        TiebaDetailInfo.objects.create(
            tid = job[0],
            comAuthor = job[1],
            comAuthorImg = job[2],
            comContent = job[3],
            comAddress = job[4],
            comTime = job[5],
        )





def init(self):
    if not os.path.exists('结果/tiebaDetail.csv'):  # 判断文件是否存在
        with open('结果/tiebaDetail.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)  # 写入表头
            print("写入表头")
            writer.writerow([ "tid", "comAuthor", "comAuthorImg", "comContent", "comAddress", "comTime"])
            print("文件创建成功")
    else:
        print("文件已存在")

if __name__ == '__main__':  # 测试
    df = pd.read_csv('结果/tieba.csv')
    column_1 = df.iloc[:, 1].tolist()  # 获取贴吧帖子爬虫数据第一列数据

    #column_1 = [9256898297]  # 自定义查找

    for tid in column_1:
        for page in range(1,page_count): #查找的页数，要想爬全部下来，要修改
            spider_out(tid,page)
            time.sleep(2)