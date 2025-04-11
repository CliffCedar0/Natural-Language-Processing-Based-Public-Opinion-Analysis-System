import csv
import jieba
import pandas as pd

with open('结果/tiebaDetail.csv', 'r', encoding='utf-8') as fp: #热词排序，把文件名改了可以看其他的
    reader = csv.reader(fp)
    content = [row[3] for row in reader]

text = ''
for i in content:
    text += i

fp.close()
lst = jieba.lcut(text)
lst = [word for word in lst if len(word) >= 2]

d_sict = {}
for key in lst:
    d_sict[key] = d_sict.get(key, 0) + 1

punc_list = ['，', '…', '。', '！', '？', '、', '；', '：', '（', '）', '【', '】', '“', '”', '‘', '’', '《', '》', '(', ')', '[', ']',
         '{', '}', '<', '>', '|', '/', '\\', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', '`', '~', ',', '.',
         '!', '?', ';', ':', '「', '」']
for i in punc_list:
    if d_sict.get(i,0) != 0:
        d_sict.pop(i)

key = list(d_sict.keys())
value = list(d_sict.values())

print(d_sict)
result = pd.DataFrame()
result['word'] = key
result['count'] = value
result.to_csv('./hotWordWeibo.csv')

data = pd.read_csv('结果/hotWordWeibo.csv', encoding='utf-8')

sorted_data = data.sort_values(by=data.columns[2],ascending=False)

sorted_data.to_csv('./hotWordWeibo.csv',index=False,encoding='utf-8')
