# 计算 predicted_sentiment 和 label 列对不上的百分比
# 假设真实标签列为 df['label'], 并且 predicted_sentiment 已经通过模型计算

import pandas as pd

df = pd.read_csv(r'789.csv')

# 计算不匹配的数量
mismatches = (df['scores'] != df['label']).sum()

# 计算总数
total = len(df)

# 计算不匹配的百分比
mismatch_percentage = (mismatches / total) * 100

# 输出结果
print(f"Predicted sentiment and label mismatch percentage: {mismatch_percentage:.2f}%")
