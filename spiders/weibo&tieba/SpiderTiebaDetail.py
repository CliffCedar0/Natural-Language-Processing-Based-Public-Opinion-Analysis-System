import os
import csv
import time
import json
import datetime
import requests
import traceback
import pandas as pd
from lxml import etree

#标头一定得对，不然无法爬取
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.259.400 QQBrowser/12.6.5708.400',
    'cookie':'XFI=caf32fd0-adac-11ef-83ea-71f301440c97; XFT=Rbybt1dXUIFRXO4aKVONoX6YmB7Q0+gJ5BvSgGcz4b4=; XFCS=46A84D472AF9519A1A15823852997A719095F9C2295DD09E8A73FB38F79BA6D1; PSTM=1646078547; BIDUPSID=09DCB1EE251B734D840C7E28D9FE98B5; BAIDUID=A40F6F3DA374B596F35D4E0EA42B78CC:FG=1; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1713948891; BDUSS=29aWW04fjRQMUYyNERSeS1hRVdsb0hTWkh0cFhjfllZY2VDdGN4dWw3dUFVZ0puSVFBQUFBJCQAAAAAAAAAAAEAAABoJmxrbG92ZWh1adbtAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIDF2maAxdpmN; BDUSS_BFESS=29aWW04fjRQMUYyNERSeS1hRVdsb0hTWkh0cFhjfllZY2VDdGN4dWw3dUFVZ0puSVFBQUFBJCQAAAAAAAAAAAEAAABoJmxrbG92ZWh1adbtAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIDF2maAxdpmN; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; H_WISE_SIDS=61027_61098_61141_61218_61206_61210_61209_61214_61243_61187_61285; H_WISE_SIDS_BFESS=61027_61098_61141_61218_61206_61210_61209_61214_61243_61187_61285; STOKEN=37ed43ba61766686c683d1a870fdaae09e0adcd8d220f8671d672cb8274d20ad; TIEBAUID=c9d819079c2a04f656236b67; IS_NEW_USER=4a22c8fc1d8bee4b290bc5ac; USER_JUMP=-1; Hm_lvt_292b2e1608b0823c1cb6beef7243ef34=1732637042,1732699672; HMACCOUNT=9E22B6998622297B; st_key_id=17; 1802249832_FRSVideoUploadTip=1; video_bubble1802249832=1; Hm_lvt_049d6c0ca81a94ed2a9b8ae61b3553a5=1732637477,1732699838; SEENKW=%E6%8A%97%E5%8E%8B%E8%83%8C%E9%94%85; Hm_lpvt_049d6c0ca81a94ed2a9b8ae61b3553a5=1732703675; tb_as_data=ab6dd2afb4e9e4ec3dc3386e2bb3869ffbc1a85a5c78ade2918a620ceb75cd0b403df22b1ba4b283d660800555af47d24caac85b1941d1e70a62f458d389f9348df6a80739117a762773af37369d7dbd937f7366f534d54eb3874ebaf5588e043e081aa7d7e99f02f0af0cbbdd0f90130d94cb6af2b9ed5e59d4c71324db4a53; BAIDUID_BFESS=A40F6F3DA374B596F35D4E0EA42B78CC:FG=1; BAIDU_WISE_UID=wapp_1732720502580_944; wise_device=0; delPer=0; PSINO=3; H_PS_PSSID=61027_61098_61141_61218_61206_61210_61209_61214_61243_61187_61285; BDRCVFR[S_ukKV6dOkf]=PfwjKziWnFsTgD8mvqV; arialoadData=false; XFI=9f48c020-adac-11ef-af66-93b0eff3a0f7; XFCS=A0B3846D10EFB9A2C7CF604B031CCA1E386A70E8E322F8C3FAF36615D1B0D6A8; XFT=XIUq9ygNzgUo6kVxZwhhaFdalmKd/hbIJpmyg+texro=; ZFY=4SYUNra9WJnpOBXYME8YYqVJXDd3I4cEnIgweC3rGU0:C; Hm_lpvt_292b2e1608b0823c1cb6beef7243ef34=1732814311; BA_HECTOR=242ha5848g2g850l01808la096bomf1jkh9f81v; ab_sr=1.0.1_NWU5NGFjODFmNWU0NzNmODk3ZWNiZDcwNDRhMTM5MDM5Nzk0ZDFiOTEwMjE5MjYxYzcwMzg0ZTJiNWMwMDI4ZTY1ZDU5NDg4NGYzMThiNjdjMjI4YmI2MDk2YjExM2MwMDM1N2Q0NTdhMDU2NGVkNjE0YTY5ZmE1YjFmZWIxMWUyNmUxMWM2YTE0MjQ1YzM1MTY0N2RiYmUxYWI2NWE5ZmRhOGU2YWJkZTNiNjM2NWRhNWE0Y2I5YjIxMWM3Yzky; st_data=afddcafc3251a42ccbc9aac9fd0c64cbb10fae7afc46538ea792e8c2074080a27e2b89ba991ded1cf9533cee840c7707c38551f8968f51c8ce61719211d705e86e5d90138d26ae2a22278705f3e378240213bdb552852fa8126ba4518479705c7dd3d23bfeb8377dee6b5c66e1143b12683bead993e0324d38fe9a46183bad84c0fe96118c1eb8cd4a27dd9afa87ed4c; st_sign=dcf7cbd2; BCLID=11241485408809503359; BCLID_BFESS=11241485408809503359; BDSFRCVID=i9AOJeCT5GWPSYRJsWzru7qCnGILeajTTPjcTR5qJ04BtyCVdP9UEG0PtDqAucFMrjJcogKK0mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=i9AOJeCT5GWPSYRJsWzru7qCnGILeajTTPjcTR5qJ04BtyCVdP9UEG0PtDqAucFMrjJcogKK0mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=JbI8VCDbJKvbfP0k-4QEbbQH-UnLqhRMWmOZ0lOmJl05hPbM3M653T_r5HJD3-6xWmJ-3RcmQUJ8HUb-jJQkD50Y5hrmLt3pBej4KKJxbpbaEt5nQCcs5Du9hUJiB5OLBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC0GejuaDTbM5pJfetjK2CntsJOOaCv8EDnOy4oT35L1DNbJQp3Z-avEQ4K5-lO_spTsbtQ83h0rMxbnQjQDWJ4J5tbX0MQfSlrEQft20b0vKtQt5MKL2TILbb7jWhk2Dq72y5jvQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCft6F8tRAfV-35b5rDHJTg5DTjhPrMXecRWMT-0aPtKK8bbUJxO4O52ljhjn_dh4JAWPQK2HnnbncJQU_hqqFxjM5M2ftZbbjwWxQxtNRJKPjpbROPKJnGqqbobUPUDMc9LUkqW2cdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLJKKBbDDRjTRb5nbH-xQ0KnLXKKOLVb3q0h7keqO2jft5Dn0r3-6eLbTxbRvD5brTWlRqHJc23h38-p0wjqQZJT3GbT5m-JbCBq6psIJM5MOaLJLSQmc3-CrgaKviaKJEBMb1MlvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe63WjNLOtTKqf5vfL5rtKRTffjrnhPF3MjFFXP6-3h0t3avTbMT4WtORJ4oGjnQThx-PXMoKaq3nLIQ2-U_a-lF2Mhom2fb4bhO-3toxJpOJ3T6CLROIB4o8OROvbURvD-ug3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqCP5bDOP; H_BDCLCKID_SF_BFESS=JbI8VCDbJKvbfP0k-4QEbbQH-UnLqhRMWmOZ0lOmJl05hPbM3M653T_r5HJD3-6xWmJ-3RcmQUJ8HUb-jJQkD50Y5hrmLt3pBej4KKJxbpbaEt5nQCcs5Du9hUJiB5OLBan7_qvIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtpChbC0GejuaDTbM5pJfetjK2CntsJOOaCv8EDnOy4oT35L1DNbJQp3Z-avEQ4K5-lO_spTsbtQ83h0rMxbnQjQDWJ4J5tbX0MQfSlrEQft20b0vKtQt5MKL2TILbb7jWhk2Dq72y5jvQlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8IjHCft6F8tRAfV-35b5rDHJTg5DTjhPrMXecRWMT-0aPtKK8bbUJxO4O52ljhjn_dh4JAWPQK2HnnbncJQU_hqqFxjM5M2ftZbbjwWxQxtNRJKPjpbROPKJnGqqbobUPUDMc9LUkqW2cdot5yBbc8eIna5hjkbfJBQttjQn3hfIkj2CKLJKKBbDDRjTRb5nbH-xQ0KnLXKKOLVb3q0h7keqO2jft5Dn0r3-6eLbTxbRvD5brTWlRqHJc23h38-p0wjqQZJT3GbT5m-JbCBq6psIJM5MOaLJLSQmc3-CrgaKviaKJEBMb1MlvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe63WjNLOtTKqf5vfL5rtKRTffjrnhPF3MjFFXP6-3h0t3avTbMT4WtORJ4oGjnQThx-PXMoKaq3nLIQ2-U_a-lF2Mhom2fb4bhO-3toxJpOJ3T6CLROIB4o8OROvbURvD-ug3-AqBM5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-jBRIE3-oJqCP5bDOP; RT="z=1&dm=baidu.com&si=a081131f-7020-45c0-9e33-a39137a861c0&ss=m41kus88&sl=h&tt=br0&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=1wtd&ul=1xja"'
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
        print("正在爬取帖子id:%d的页面第%d条数据" % (tid,index + 1))
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
    with open('../Outcome/tiebaDetail.csv', 'a', newline ='', encoding='utf-8') as wf:
        writer = csv.writer(wf)#
        writer.writerow(rowData)#写入数据

def clear_csv(self):
    df = pd.read_csv('../Outcome/tiebaDetail.csv')
    df.drop_duplicates(inplace=True)
    print("总数据为%d" % df.shape[0])
    return df.values

def init():
    if not os.path.exists('../Outcome/tiebaDetail.csv'):  # 判断文件是否存在
        with open('../Outcome/tiebaDetail.csv', 'a', newline='', encoding='utf-8') as wf:
            writer = csv.writer(wf)  # 写入表头
            writer.writerow([ "tid", "comAuthor", "comAuthorImg", "comContent", "comAddress", "comTime"])

if __name__ == '__main__':  # 测试
    init()
    df = pd.read_csv('../Outcome/tieba.csv')
    column_1 = df.iloc[:, 1].tolist()  # 获取贴吧帖子爬虫数据第一列数据
    #column_1 = [9256898297]  # 自定义查找
    page_count = 2
    for tid in column_1:
        for page in range(1,page_count): #查找的页数，要想爬全部下来，要修改
            spider_out(tid,page)
            time.sleep(2)