import pandas as pd


df1 = pd.read_csv('task1_1_1.csv', encoding='gbk')
df2 = pd.read_csv('task1_1_2.csv', encoding='gbk')
df3 = pd.read_csv('task1_1_3.csv', encoding='gbk')
df4 = pd.read_csv('task1_2_1.csv', encoding='gbk')
df5 = pd.read_csv('task1_2_2.csv', encoding='gbk')

df1.to_csv('task1.csv', encoding='utf8', index=False)
df2.to_csv('task2.csv', encoding='utf8', index=False)
df3.to_csv('task3.csv', encoding='utf8', index=False)
df4.to_csv('task4.csv', encoding='utf8', index=False)
df5.to_csv('task5.csv', encoding='utf8', index=False)




















