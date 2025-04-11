import pandas as pd
def clean_text():
    file = ['weibo', 'tieba']
    for i in range(0,2):
        df = pd.read_csv(f'../Outcome/{file[i]}.csv', encoding='utf-8')
        colum_index = 5
        # 去掉换行和缩进
        df['content'] = df.iloc[:, colum_index].astype(str).str.replace('\n\r', '', regex=False)
        df['content'] = df['content'].str.replace('\r', '', regex=False)
        df['content'] = df['content'].str.replace('\n', '', regex=False)
        df.to_csv(f'../Outcome/{file[i]}New.csv', encoding='utf-8',index=False)

if __name__ == '__main__':
    clean_text()