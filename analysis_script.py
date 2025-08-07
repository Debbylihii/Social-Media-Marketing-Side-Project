import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import os
import matplotlib.font_manager as fm

# 修正中文顯示問題
# -------------------------------------------------------------
def find_chinese_font():
    """尋找系統中可用的繁體中文字型"""
    font_names = ['Microsoft JhengHei', 'DFKai-SB', 'PingFang TC', 'Arial Unicode MS', 'WenQuanYi Zen Hei']
    for font_name in font_names:
        if any(font_name in f.name for f in fm.fontManager.ttflist):
            return font_name
    return None

chinese_font = find_chinese_font()
if chinese_font:
    plt.rcParams['font.sans-serif'] = [chinese_font, 'Arial'] # 優先使用找到的字型
    plt.rcParams['axes.unicode_minus'] = False # 正常顯示負號
else:
    print("警告：系統中未找到合適的繁體中文字型，圖表中的中文字可能無法正常顯示。")

# 1. 生成模擬資料
# -------------------------------------------------------------
np.random.seed(42)  # 確保每次生成的資料都相同

# 定義貼文類型與發文時間
post_types = ['課程介紹', '課後花絮', '教養小知識', '活動文']
post_times = ['早上', '下午']

data = []
for i in range(50):
    post_type = np.random.choice(post_types, p=[0.4, 0.2, 0.2, 0.2])
    post_time = np.random.choice(post_times)

    # 根據貼文類型生成互動數
    if post_type == '課程介紹':
        interactions = np.random.randint(50, 200)
    else:
        interactions = np.random.randint(20, 100)

    # 根據發文時間和貼文類型生成報名數
    if post_time == '早上':
        if post_type == '課程介紹':
            registrations = max(0, int(interactions * np.random.uniform(0.12, 0.35) + np.random.normal(7, 5)))
        else:
            registrations = max(0, int(interactions * np.random.uniform(0.07, 0.18) + np.random.normal(3, 3)))
    else:
        if post_type == '課程介紹':
            registrations = max(0, int(interactions * np.random.uniform(0.1, 0.3) + np.random.normal(5, 5)))
        else:
            registrations = max(0, int(interactions * np.random.uniform(0.05, 0.15) + np.random.normal(2, 3)))

    data.append([post_type, post_time, interactions, registrations])

df = pd.DataFrame(data, columns=['貼文類型', '發文時間', '互動數', '報名數'])

print("--- 模擬資料預覽 ---")
print(df.head())
print("\n")

# 建立儲存圖表的資料夾
if not os.path.exists('output'):
    os.makedirs('output')

# 2. 數據分析與視覺化
# -------------------------------------------------------------

# 問題一：哪類貼文報名轉換率最高？
plt.figure(figsize=(10, 6))
avg_registrations_by_type = df.groupby('貼文類型')['報名數'].mean().sort_values(ascending=False)
sns.barplot(x=avg_registrations_by_type.index, y=avg_registrations_by_type.values, palette='viridis')
plt.title('貼文類型 vs. 平均報名數', fontsize=16)
plt.xlabel('貼文類型', fontsize=12)
plt.ylabel('平均報名數', fontsize=12)
plt.xticks(rotation=45)
plt.savefig('output/post_type_vs_registrations.png', bbox_inches='tight')
plt.show()

print("--- 平均報名數統計 ---")
print(avg_registrations_by_type)
print("\n")

# 問題二：發文時間是否影響報名？
plt.figure(figsize=(8, 5))
avg_registrations_by_time = df.groupby('發文時間')['報名數'].mean().sort_values(ascending=False)
sns.barplot(x=avg_registrations_by_time.index, y=avg_registrations_by_time.values, palette='magma')
plt.title('發文時間 vs. 平均報名數', fontsize=16)
plt.xlabel('發文時間', fontsize=12)
plt.ylabel('平均報名數', fontsize=12)
plt.savefig('output/post_time_vs_registrations.png', bbox_inches='tight')
plt.show()

print("--- 不同時段平均報名數統計 ---")
print(avg_registrations_by_time)
print("\n")

# 問題三：互動數是否與報名數有正相關？
plt.figure(figsize=(10, 6))
sns.scatterplot(x='互動數', y='報名數', hue='貼文類型', data=df, s=100)
plt.title('互動數 vs. 報名數散佈圖', fontsize=16)
plt.xlabel('互動數', fontsize=12)
plt.ylabel('報名數', fontsize=12)
plt.legend(title='貼文類型')
plt.savefig('output/interactions_vs_registrations.png', bbox_inches='tight')
plt.show()

# 計算皮爾森相關係數
corr, _ = pearsonr(df['互動數'], df['報名數'])
print(f"--- 互動數與報名數的相關係數： {corr:.2f} ---")
print("\n")