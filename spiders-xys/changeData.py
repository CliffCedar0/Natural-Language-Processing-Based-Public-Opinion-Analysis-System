import pandas as pd

df = pd.read_csv('结果/weibo.csv', encoding='utf-8')

column_index = 5

df['content'] = df.iloc[:,column_index].astype(str).str.replace('\r\n', '',regex=False)
df['content'] = df['content'].str.replace('\n', '',regex=False)
df['content'] = df['content'].str.replace('\r', '',regex=False)

df.to_csv('weiboNew.csv',index=False,encoding='utf-8')