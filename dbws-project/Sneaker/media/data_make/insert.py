import csv
import codecs
import mysql.connector
config={'host':'127.0.0.1',#默认127.0.0.1
        'user':'root',
        'password':'1q2w3e',
        'port':3306 ,#默认即为3306
        'database':'project',
        'auth_plugin':'mysql_native_password'}

def Insert_seller_csv():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        csvfile0 = codecs.open('shop_seller.csv', 'r', 'utf-8-sig')
        dreader = csv.DictReader(csvfile0)
        to_db = [(i['seller_id'], i['username'], i['passwd'], i['Address'], i['c_time']) for i in dreader]
        print(dreader)
        print(type(to_db))
        print(to_db)
        cursor.executemany("INSERT INTO seller(id, username, Passwd, Address, c_time)VALUES (?,?,?,?,?);", to_db)
        connection.commit()  # save the change permanently
    finally:
        connection.close()  # DO NOT forget to close the connection.
        print("Success to insert seller_data")
    return "Success to insert the seller_data"
Insert_seller_csv()