import pandas as pd
import datetime
import time
import requests
import os
import mysql.connector
#fill nan
sneakers=pd.read_csv(".\\data_make\\shop_sneaker.csv")
sneakers['price'].fillna(int(sneakers['price'].mean()))
c=0

#download picture

for i in sneakers.index:
    url=sneakers.loc[i,'imag']
    if not pd.isna(url):
        file='.\\img\\{}.jpg'.format(sneakers.loc[i,'name'])
        if not os.path.exists(file):
            r=requests.get(url)
            if r.status_code==200:
                try:
                    open(file,'wb').write(r.content)
                    c+=1
                    print(c)
                except:
                    print(file)

#import sneaker
config={'host':'127.0.0.1',
        'user':'root',
        'password':'1q2w3e', #If it is a new user, please change the password and name, and set up the database in advance.
        'port':3306 ,
        'database':'project',
        'auth_plugin':'mysql_native_password'}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
for i in sneakers.index:
    if not pd.isna(sneakers.loc[i,'imag']):
        sql_command = 'INSERT INTO shop_sneaker VALUES ({id},"{name}","{price}", "{brand}", "img/{img}.jpg");'.format(id=i+1,name=sneakers.loc[i,'name'],
                                                                                                                 brand=sneakers.loc[i,'brand'],
                                                                                                                 price=sneakers.loc[i,'price'],
                                                                                                                 img=sneakers.loc[i,'name'])
    else:
        sql_command = 'INSERT INTO shop_sneaker VALUES ({id},"{name}","{price}", "{brand}", "img/504.jpg");'.format(id=i+1,name=sneakers.loc[i,'name'],
                                                                                                                 brand=sneakers.loc[i,'brand'],
                                                                                                                 price=sneakers.loc[i,'price'],
                                                                                                                 )
    cursor.execute(sql_command)
    print(c)
    c += 1
connection.commit()
connection.close()

#import buyer and seller
buyer=pd.read_csv(".\\data_make\\shop_buyer.csv")
seller=pd.read_csv(".\\data_make\\shop_seller.csv")
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
c=0
print(buyer)
for i in buyer.index:
    year,month,day=time.strptime(buyer.loc[i,'c_time'],'%m/%d/%Y')[:3]
    date=datetime.date(year,month,day)
    print(date)
    sql_command = 'INSERT INTO shop_buyer(id,username,password,address,c_time) VALUES ({userid},"{username}","{password}","{address}","{c_time}");'.format(userid=buyer.loc[i,'buyer_id'],
                                                                                                                                             username=buyer.loc[i,'username'],
                                                                                                                                             password=buyer.loc[i,'passwd'],
                                                                                                                                             address=buyer.loc[i,'address'],
                                                                                                                                             c_time=date
                                                                                                                                             )
    print(sql_command)
    cursor.execute(sql_command)
    print(c)
    c+=1
connection.commit()
for i in seller.index:
    year, month, day = time.strptime(seller.loc[i, 'c_time'], '%m/%d/%Y')[:3]
    date = datetime.date(year, month, day)
    sql_command = 'INSERT INTO shop_seller(id,username,password,address,c_time) VALUES ({userid},"{username}","{password}","{address}","{c_time}");'.format(userid=seller.loc[i,'seller_id'],
                                                                                                                                             username=seller.loc[i,'username'],
                                                                                                                                             password=seller.loc[i,'passwd'],
                                                                                                                                             address=seller.loc[i,'Address'],
                                                                                                                                             c_time=date
                                                                                                                                             )
    print(sql_command)
    cursor.execute(sql_command)
    #print(c)
    c+=1
connection.commit()
connection.close()
#inport inventory
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
c=0
inventory=pd.read_csv(".\\data_make\\inventory.csv")
print(inventory)
for i in inventory.index:
    sql_command = 'INSERT INTO shop_inventory(id,seller_id,sneakerid_id) VALUES ({id},"{seller}",{sneakerid});'.format(id=inventory.loc[i,'id'],
                                                                                                                        sneakerid=inventory.loc[i,'sneaker_id'],
                                                                                                                        seller=inventory.loc[i,'seller_id'])
    print(sql_command)
    cursor.execute(sql_command)
    print(c)
    c+=1
connection.commit()
connection.close()

#import customization
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
c=0
custom=pd.read_csv(".\\data_make\\manufacturer.csv")
print(custom)
for i in custom.index:
    sql_command = 'INSERT INTO shop_customization(id,color) VALUES ({id},"{color}");'.format(id=custom.loc[i,'Manufacturer_id'],
                                                                                        color=custom.loc[i,'color'])
    print(sql_command)
    cursor.execute(sql_command)
    print(c)
    c+=1
connection.commit()
connection.close()
#import sold
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
c=0
sold=pd.read_csv(".\\data_make\\shop_sold.csv")
print(sold)
for i in sold.index:
    sql_command = 'INSERT INTO shop_sold(soldid,sneakerid_id) VALUES ({id},{sneakerid});'.format(id=sold.loc[i,'sold_id'],
                                                                                                sneakerid=sold.loc[i,'sneakerid_id'])
    print(sql_command)
    cursor.execute(sql_command)
    print(c)
    c+=1
connection.commit()
connection.close()

#import order
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
c=0
order=pd.read_csv(".\\data_make\\shop_order.csv")
print(order)
for i in order.index:
    year, month, day = time.strptime(order.loc[i, 'c_time'], '%m/%d/%Y')[:3]
    date = datetime.date(year, month, day)
    if not pd.isna(order.loc[i,'manufacturer_id']):
        sql_command = 'INSERT INTO shop_order(id,c_time,buyer_id,custom_id,inventoryid_id,seller_id) VALUES ({id},"{c_time}","{buyer}",{custom},{inventory},"{seller}");'.format(id=order.loc[i,'Order_id'],
                                                                                                                                                c_time=date,
                                                                                                                                                buyer=order.loc[i,'buyer_id'],
                                                                                                                                                custom=order.loc[i,'manufacturer_id'],
                                                                                                                                                seller=order.loc[i,'seller_id'],
                                                                                                                                                inventory=order.loc[i,'inventoryid_id'])
        print(sql_command)
        cursor.execute(sql_command)
        c+=1
        print(c)
    else:
        sql_command = 'INSERT INTO shop_order(id,c_time,buyer_id,inventoryid_id,seller_id) VALUES ({id},"{c_time}","{buyer}",{inventory},"{seller}");'.format(
            id=order.loc[i, 'Order_id'],
            c_time=date,
            buyer=order.loc[i, 'buyer_id'],
            seller=order.loc[i, 'seller_id'],
            inventory=order.loc[i, 'inventoryid_id'])
        print(sql_command)
        cursor.execute(sql_command)
        c+=1
        print(c)
connection.commit()
connection.close()

