from bs4 import BeautifulSoup
import requests
import pandas as pd
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

browser = webdriver.Edge('.\msedgedriver.exe')
browser.get("https://sneakercon.com/shop")
for i in range(500):#refresh the page
    try:
        button = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.LINK_TEXT, 'Load More')))
        button.click()
        print(i)
    except Exception:
        continue
r=browser.page_source
name=[]
price=[]
brand=[]
code=[]
imag=[]
soup = BeautifulSoup(r, "html.parser")
rows = soup.find('div', class_='shop-items-grid')
rows=rows.find_all('div',{'class':'product-cell'})
for row in rows:# get infomation from htnl
    name.append(row.find('span', {'class': "product-cell__item-name"}).text.strip())
    if (row.find('span', {'class':"product-cell__item-button product-cell__item-button--price"})):
        price.append(row.find('span', {'class':"product-cell__item-button product-cell__item-button--price"}).text.strip())
    else:
        price.append(None)
    if (row.find('span', {'class': "product-cell__item-brand"})):
        brand.append(row.find('span', {'class': "product-cell__item-brand"}).text.strip())
    else:
        brand.append(None)
    code.append(row.find('span', {'class': "product-cell__item-code"}).text.strip())
    if(row.find('img', {'alt':'dunk-humidity'})):
        imag.append(row.find('img', {'alt':'dunk-humidity'}).get("src"))
    else:
        imag.append(None)
result2 = pd.DataFrame({"name": name, 'price': price,'brand': brand,'code': code,'imag': imag})
result2.to_csv("sneaker.csv")
