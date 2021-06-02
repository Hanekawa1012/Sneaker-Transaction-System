import os
import pandas as pd
import random

A = []
for i in range(1, 5599):
    A.append(i)

B = []
for i in range(1, 5599):
    a = str(i)
    B.append('Davis'+a)

C = []
for i in range(1, 5599):
    C.append(123456)

data = {'seller_id': A, 'username': B, 'passwd': C}
df = pd.DataFrame(data, columns=['seller_id', 'username', 'passwd'])
print(df)
if os.path.exists('shop_seller.csv'):
    os.remove('shop_seller.csv')
df.to_csv('shop_seller.csv', encoding='utf-8-sig')
