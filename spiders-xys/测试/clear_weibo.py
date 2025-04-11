import pandas as pd
import os


try:
    # 尝试读取CSV文件到DataFrame
    df = pd.read_csv('..\结果\processed_weibo.csv')
    # 只保留content列
    df = df[['content']]
    # 显示结果
    print(df)
    # 如果需要，可以将结果保存到新的CSV文件
    df.to_csv('data_cleaned.csv', index=False)
except FileNotFoundError:
    print("错误：文件未找到，请检查文件路径是否正确。")
except pd.errors.EmptyDataError:
    print("错误：文件是空的。")
except Exception as e:
    print(f"发生了一个错误：{e}")
