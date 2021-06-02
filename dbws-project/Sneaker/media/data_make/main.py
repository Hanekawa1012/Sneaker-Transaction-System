import os
import pandas as pd
import random

A = []
for i in range(1, 6001):
    A.append(i)

B = []
for i in range(1, 6001):
    a = str(i)
    B.append('Barry'+a)

C = []
for i in range(1, 6001):
    C.append(1234)

data = {'buyer_id': A, 'username': B, 'passwd': C}
df = pd.DataFrame(data, columns=['buyer_id', 'username', 'passwd'])
print(df)
if os.path.exists('shop_buyer.csv'):
    os.remove('shop_buyer.csv')
df.to_csv('shop_buyer.csv', encoding='utf-8-sig')
