from flask import Flask, jsonify, request
import requests
from lxml import etree
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'cookie': 'SCF=AryeBeMawiC3YM1mnPJRAdR9KAFcZrT6tKVXlvcTePuydHmshKRQVVw-VIw_XUFkmGYBeHS_D5FZd2e8WS5-Uq8.; SINAGLOBAL=2194215254634.737.1731132648527; SUB=_2A25KbtbZDeRhGeBN7FYR9CrPyTWIHXVpAlYRrDV8PUNbmtAYLXPekW9NRDr1RzYY_lvUNy9kkx7bou9HLXFxZRPr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5PiwnjJ2PvMV53L248EaXP5NHD95Qce0MXehBXe0z4Ws4DqcjGTHyHPfHqTBtt; ALF=02_1737634697; _s_tentry=passport.weibo.com; Apache=5770074436449.757.1735042698403; ULV=1735042698412:3:1:1:5770074436449.757.1735042698403:1731136587912; XSRF-TOKEN=Ce_HxXptIV0_PPYqTyZBXGi2; WBPSESS=xk-Ldgm3Q0QVwpDD_1JOWqXY2_fntD9mJY7j1-8WMf1P7D6S2kZiPBledHc8ThhYX2F9cfpEd8iuS_d8O0nR-ksnMowpenDeq0IOg8-orPfXs0Z0_1wrKKabKwHdw4hkircyWLoq4r9d94HM3UFB2g=='
}

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
    Reading = url_list[0].text if url_list else "无"
    Discussion = url_list[1].text if len(url_list) > 1 else "无"
    return Reading, Discussion

@app.route('/weibo-hot', methods=['POST'])
def weibo_hot():
    url = 'https://weibo.com/ajax/side/hotSearch'
    response = get_data(url)
    if response:
        hot_list = []
        hotgov = response['data']['hotgov']
        name = hotgov['name']
        url = "https://s.weibo.com/weibo?q=%23" + name[1:-1] + "%23"
        Reading, Discussion = get_url(url)
        hot_list.append({"name": name, "url": url, "Reading": Reading, "Discussion": Discussion})

        hotList = response['data']['realtime']
        for hot in hotList:
            name = hot['word']
            url = "https://s.weibo.com/weibo?q=%23" + name + "%23"
            try:
                Reading, Discussion = get_url(url)
            except Exception as e:
                Reading = "无"
                Discussion = "无"
            hot_list.append({"name": name, "url": url, "Reading": Reading, "Discussion": Discussion})

        return jsonify(hot_list)
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
