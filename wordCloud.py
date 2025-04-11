import re
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from utils.querys import querylocaldb


def get_img(targetImageSec, resImageSrcs, stopwords_file_path):
    # 从数据库获取数据
    data1 = querylocaldb('select comContent from tiebaComment', [], 'select')
    data2 = querylocaldb('select content from weiboComment', [], 'select')
    data = data1 + data2

    # 将数据转换为字符串
    text = ''
    for i in data:
        try:
            if i[0] != '':
                tarArr = i
                for j in tarArr:
                    text += j
        except:
            continue

    # 读取停用词文件
    with open(stopwords_file_path, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())

    # 分词
    data_cut = jieba.cut(text, cut_all=False)

    # 过滤停用词
    words = [word for word in data_cut if word not in stopwords]
    # 过滤掉长度小于2的词
    filtered_words = [word for word in words if len(word) >= 2]
    # 过滤掉纯英文的分词
    filtered_words = [word for word in filtered_words if not re.match(r'^[a-zA-Z]+$', word)]

    # 转换为字符串
    s1 = ' '.join(filtered_words)

    # 词云图
    img = Image.open(targetImageSec)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        font_path='STHUPO.TTF',
        mask=img_arr
    )
    wc.generate_from_text(s1)

    # 绘制图
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImageSrcs, dpi=800, bbox_inches='tight', pad_inches=-0.1)


# 调用函数
stopwords_file_path = 'C:\\Users\\ASUS\\Desktop\\基于spark的舆情分析系统\\基于spark的舆情分析系统\\static\\hit_stopwords.txt'
get_img('C:\\Users\\ASUS\\Desktop\\基于spark的舆情分析系统\\基于spark的舆情分析系统\\static\\love.jpg',
        './static/assets/cloudImg/11', stopwords_file_path)
