import csv
import pandas as pd
import jieba

try:
    with open('../Outcome/tiebaDetail.csv', 'r', encoding='utf-8') as f:
        reader=csv.reader(f)
        content= [row[3] for row in reader]     #获取评论里的每一条内容
except:
    print("数据文件不存在！")
    exit()

text=''
for i in content:   #把内容合成一条文本方便jieba库统计
    text+=i
# print(text)
f.close()
lst=jieba.lcut(text)
lst=[word for word in lst if len(word)>=2] #提取大于等于两个字符的词


d_dict={}
for key in lst:#获取每个词出现的次数，dict.get()表示获取这个键所对应的值，这里+1做到了统计的作用
    d_dict[key]=d_dict.get(key,0)+1
#排除不需要的字符
punc_list=['，', '…', '。', '！', '？', '、', '；', '：', '（', '）', '【', '】', '“', '”', '‘', '’', '《', '》', '(', ')', '[', ']',
         '{', '}', '<', '>', '|', '/', '\\', '@', '#', '$', '%', '^', '&', '*', '+', '=', '-', '_', '`', '~', ',', '.',
         '!', '?', ';', ':', '「', '」','23','2024.07','的','了','我','@','是','都','就','1','找','2','在','有','也','看','去','还','你','']
#如果字典能获取到跟该列表一样的元素那就等于0
for i in punc_list:
    if d_dict.get(i,0)!=0:
        d_dict.pop(i)
key=list(d_dict.keys())
value=list(d_dict.values())

# print(d_dict)
resualt=pd.DataFrame()
resualt['word']=key
resualt['count']=value
resualt.to_csv('../Outcome/hotWordTieba.csv')
#保存热词并排序
data=pd.read_csv('../Outcome/hotWordTieba.csv', encoding='utf-8')
sorted_data=data.sort_values(by=data.columns[2],ascending=False)
sorted_data=sorted_data.iloc[:,1:] #去掉第一列的无用数据
sorted_data.to_csv('../Outcome/hotWordTieba.csv',index=False)
# print(sorted_data)