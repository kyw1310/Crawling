#!/usr/bin/env python
# coding: utf-8

# In[13]:


import sys
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
#import pyperclip
import time
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
import urllib
import re
import datetime





url=input('url을 입력해주세요')



options = wd.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")



driver=wd.Chrome(executable_path='./chromedriver.exe',chrome_options=options)



driver.get(url)
time.sleep(2)
total=driver.find_element_by_css_selector('#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a > span').text

total_num=int(total.replace(',',''))

#a=driver.find_element_by_css_selector('#_productTabContainer > div > div.XYLPnZFSI9 > strong').text


#driver.find_element_by_css_selector('#_productTabContainer > div > div._27jmWaPaKy._1dDHKD1iiX > ul > li:nth-child(2) > a').click()

driver.implicitly_wait(2)

print('전체리뷰수:',total_num)
x=int(input('몇개의 리뷰를 가져오시겠습니까'))

epochs=x//20

ss=x%20

result=[]
num=3
time.sleep(5)
for epoch in range(epochs+1):
    time.sleep(1)
    tt=driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > ul')
    
    htt=tt.get_attribute('outerHTML')
    html=bs(htt,'html.parser')
    stars=html.findAll('em',{'class':'_15NU42F3kT'})
    texts=html.findAll('span',{'class':'_3QDEeS6NLn'})
    
    if epoch!=epochs:
        
        for review in range(20):

            star=int(stars[review].text)
            text=texts[2*review+1].text
            result.append([star,text])
    else:
        for review in range(ss):
            star=int(stars[review].text)
            text=texts[2*review+1].text
            result.append([star,text])
        break
    
    if num%12!=0:
        driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > a:nth-child('+str(num)+')').click()
        time.sleep(1)
        num+=1
    else:
        driver.find_element_by_css_selector('#REVIEW > div > div._2y6yIawL6t > div > div.cv6id6JEkg > div > div > a.fAUKm1ewwo._2Ar8-aEUTq').click()
        time.sleep(1)
        num=3
        
driver.close()
df=pd.DataFrame(result,columns=['별점','리뷰'])

now=datetime.datetime.now()

time_=('%02d%02d%02d-%02d%02d%02d' %(int(str(now.year)[2:]),now.month,now.day,now.hour,now.minute,now.second))
a=input('엑셀파일 이름을 입력해주세요')
print('완료됐습니다')

df.to_excel(time_+'_'+a+'.xlsx',index=None)

