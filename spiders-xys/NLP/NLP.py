import pandas as pd
from snownlp import SnowNLP

def getemotion():
    df = pd.read_csv('../NLP/项目数据/weibodata.csv', encoding='UTF-8')
    # df = df[:100]
    scores = []
    third_column = df.iloc[:, 5]
    for content in third_column:
        content = str(content)
        s = SnowNLP(content)
        # 只添加一次，根据s.sentiments的值来决定是1还是0
        # if s.sentiments > 0.5:
        #     scores.append(1)
        # else:
        #     scores.append(0)
        scores.append(s.sentiments)

    df['scores1'] = scores

    df.to_csv('weibodataNewNLP.csv', index=False)
    print("情感分析完成，结果已保存至 weibodataNewNLP.csv")

getemotion()
