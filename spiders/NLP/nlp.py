import pandas as pd
from snownlp import SnowNLP

def get_emotion_weibo():
    df=pd.read_csv('../Outcome/weiboNew.csv') #读取评论热词
    scores=[]
    for content in df['content']:
        content=str(content) # 确保内容是字符串
        s=SnowNLP(content)
        scores.append(s.sentiments) # 使用sentiments属性获取情感分析得分并添加到列表中

    df['scores']=scores
    df.to_csv('NLP_weibo.csv',index=False)

def get_emotion_weiboWord():
    df=pd.read_csv('../Outcome/HotWordweibo.csv') #读取评论热词
    scores=[]
    for content in df['word']:
        content=str(content) # 确保内容是字符串
        s=SnowNLP(content)
        scores.append(s.sentiments) # 使用sentiments属性获取情感分析得分并添加到列表中

    df['scores']=scores
    df.to_csv('NLP_hotWordWeibo.csv',index=False)

def get_emotion_tieba():
    df=pd.read_csv('../Outcome/tiebaNew.csv') #读取评论热词
    scores=[]
    for content in df['title']:
        content=str(content) # 确保内容是字符串
        s=SnowNLP(content)
        scores.append(s.sentiments) # 使用sentiments属性获取情感分析得分并添加到列表中

    df['scores']=scores
    df.to_csv('NLP_Tieba.csv',index=False)

def get_emotion_tiebaWord():
    df=pd.read_csv('../Outcome/HotWordTieba.csv') #读取评论热词
    scores=[]
    for content in df['word']:
        content=str(content) # 确保内容是字符串
        s=SnowNLP(content)
        scores.append(s.sentiments) # 使用sentiments属性获取情感分析得分并添加到列表中

    df['scores']=scores
    df.to_csv('NLP_hotWordTieba.csv',index=False)

if __name__ == '__main__':
    get_emotion_weibo()
    get_emotion_tieba()
    get_emotion_weiboWord()
    get_emotion_tiebaWord()