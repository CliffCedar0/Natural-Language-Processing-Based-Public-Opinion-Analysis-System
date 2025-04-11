import csv
import os
import requests
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'cookie': 'SCF=AryeBeMawiC3YM1mnPJRAdR9KAFcZrT6tKVXlvcTePuydHmshKRQVVw-VIw_XUFkmGYBeHS_D5FZd2e8WS5-Uq8.; SINAGLOBAL=2194215254634.737.1731132648527; SUB=_2A25KbtbZDeRhGeBN7FYR9CrPyTWIHXVpAlYRrDV8PUNbmtAYLXPekW9NRDr1RzYY_lvUNy9kkx7bou9HLXFxZRPr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5PiwnjJ2PvMV53L248EaXP5NHD95Qce0MXehBXe0z4Ws4DqcjGTHyHPfHqTBtt; ALF=02_1737634697; _s_tentry=passport.weibo.com; Apache=5770074436449.757.1735042698403; ULV=1735042698412:3:1:1:5770074436449.757.1735042698403:1731136587912; XSRF-TOKEN=Ce_HxXptIV0_PPYqTyZBXGi2; WBPSESS=xk-Ldgm3Q0QVwpDD_1JOWqXY2_fntD9mJY7j1-8WMf1P7D6S2kZiPBledHc8ThhYX2F9cfpEd8iuS_d8O0nR-ksnMowpenDeq0IOg8-orPfXs0Z0_1wrKKabKwHdw4hkircyWLoq4r9d94HM3UFB2g=='
}


def save_to_csv(resultData):
    # 这里不需要每次都打开文件，因为文件在init函数中已经被创建
    with open('结果/weiboHot.csv', 'a', newline='', encoding='utf-8') as wf:
        writer = csv.writer(wf)
        writer.writerow(resultData)
        print("写入数据: ", resultData)


def init():
    file_path = '结果/weiboHot.csv'
    if os.path.exists(file_path):  # 如果文件存在，则删除
        os.remove(file_path)
        print("旧文件已删除")

    # 创建新文件并写入表头
    with open(file_path, 'w', newline='', encoding='utf-8') as wf:
        writer = csv.writer(wf)
        writer.writerow(["rank", "typeName","num","url"])
        print("文件创建成功并写入表头")


def get_data(url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_url(url):
    originalUrl = url
    response = requests.get(originalUrl, headers=headers, timeout=60).text
    page_tree = etree.HTML(response)

    url_list = page_tree.xpath('//div[@class="total"]/span')

    Reading = url_list[0].text
    Discussion = url_list[1].text
    return Reading,Discussion

def parse_json(response):
    hotgov = response['data']['hotgov']
    ranking = -1
    name = hotgov['name']
    num = -1
    url = "https://s.weibo.com/weibo?q=%23" + name[1:-1] + "%23"
    Reading,Discussion = get_url(url)
    save_to_csv([ranking, name, num, url, Reading, Discussion])
    hotList = response['data']['realtime']
    for hot in hotList:
        ranking = hot.get('rank', -2)  # 使用get方法提供默认值
        name = hot['word']
        num = hot['num']
        url = "https://s.weibo.com/weibo?q=%23" + name + "%23"
        try:
            Reading,Discussion = get_url(url)
        except Exception as e:
            Reading = "无"
            Discussion = "无"
        save_to_csv([ranking, name, num, url, Reading, Discussion])


if __name__ == '__main__':
    init()  # 确保每次运行都是从干净的状态开始
    url = 'https://weibo.com/ajax/side/hotSearch'
    response = get_data(url)
    if response:  # 确保有响应再进行解析
        parse_json(response)
    else:
        print("Failed to retrieve data")
