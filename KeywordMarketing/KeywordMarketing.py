#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip
import time
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import numpy as np
import urllib
import re
import datetime


# In[2]:


def copy_input(xpath,input):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)


# In[3]:


def naver_(lis):
    for i in range(len(lis)):
        if '네이버쇼핑' in lis[i]:
            return i+1
    else:
        return 0


# In[190]:


options=wd.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozila/5.0')


# In[4]:


id=input('id를 입력해주세요:')
pw=input('pw를 입력해주세요:')


# In[52]:


driver=wd.Chrome(executable_path='chromedriver.exe')


# In[53]:


driver.get('https://searchad.naver.com/')


# In[54]:


copy_input('//*[@id="uid"]',id)
time.sleep(1)
copy_input('//*[@id="upw"]',pw)
time.sleep(1)
driver.find_element_by_xpath('//*[@id="container"]/main/div/div[1]/home-login/div/fieldset/span/button').click()
time.sleep(2)


# In[55]:


try:
    driver.find_element_by_css_selector('#new\.dontsave').click()
except:
    print('no_error')


# In[56]:


driver.get('https://searchad.naver.com/')


# In[57]:


driver.find_element_by_css_selector('#header_js > div > ul > li.system > a').click()


# In[58]:


current_tab=driver.window_handles[-1]
driver.switch_to_window(window_name=current_tab)


# In[59]:


s=True
while s:
    try:
        driver.find_element_by_css_selector('#navbar-common-header-collapse > ul > li:nth-child(3) > a').click()
        s=False
    except:
        driver.close()
        current_tab=driver.window_handles[-1]
        driver.switch_to_window(window_name=current_tab)
        time.sleep(2)
time.sleep(2)


# In[60]:


driver.find_element_by_css_selector('#navbar-common-header-collapse > ul > li.ng-scope.dropdown.open > ul > li:nth-child(3) > a').click()

# In[61]:


link=driver.find_element_by_css_selector('body > elena-root > elena-wrap > div > div:nth-child(2) > elena-tool-wrap > div > div > div > div > elena-keyword-planner > div.row.lang-ko-KR > div.col-sm-9.col-keyword-query > div:nth-child(1) > div.card-body.hint-area > div > div > div:nth-child(1) > div > textarea')

# In[63]:


a=input('키워드를 입력하세요 (총다섯개까지, 띄어쓰기로 구분)')


# In[64]:


d=int(input('검색조건을 지정하시겠습니까? (Yes:1 , No:0)'))
while True:
    if d==1:
        minimum = int(input('연관키워드 월간 검색수 최소:'))
        maximum = int(input('연관키워드 월간 검색수 최대:'))
        break
    elif d==0:
        break
    else:
        print('1 , 0 중에 선택해주세요')


# In[65]:


link.clear()
link.send_keys('\n'.join(a.split()))


# In[66]:


driver.find_element_by_css_selector('body > elena-root > elena-wrap > div > div:nth-child(2) > elena-tool-wrap > div > div > div > div > elena-keyword-planner > div.row.lang-ko-KR > div.col-sm-9.col-keyword-query > div:nth-child(1) > div.card-footer > button').click()
time.sleep(2)


# In[67]:


links=driver.find_element_by_css_selector('body > elena-root > elena-wrap > div > div:nth-child(2) > elena-tool-wrap > div > div > div > div > elena-keyword-planner > div.row.lang-ko-KR > div.col-sm-9.col-keyword-query > div:nth-child(2) > div.elena-table-area > elena-table > div > div > table > tbody').text


# In[68]:


col=['연관키워드','PC월간검색수','모바일월간검색수','PC월평균클릭수','모바일월평균클릭수','PC월평균클릭률','모바일월평균클릭률','경쟁정도','월평균노출광고수']


# In[69]:


data=pd.DataFrame(np.array(links.split('\n')).reshape(-1,9),columns=col)


# In[70]:


tt=(list(map(lambda x : x.replace(',',''),data['PC월간검색수'])))


# In[71]:


data['PC월간검색수']=list(map(lambda x:0 if x=='< 10' else int(x),tt))


# In[72]:


ttt=(list(map(lambda x: x.replace(',',''),data['모바일월간검색수'])))


# In[73]:


data['모바일월간검색수']=list(map(lambda x: 0 if x=='< 10' else int(x),ttt))


# In[74]:


deldel=[]
if d==1:
    for i in range(len(data)):
        total=data.iloc[i,2]+data.iloc[i,1]
        if total < minimum or total > maximum:
            deldel.append(i)
    data.drop(deldel,axis=0,inplace=True)


# In[75]:


item_list=np.array(data['연관키워드'])


# In[76]:


store_num=[]
#blog=[]
#cafe=[]
category=[]
rank=[]
coupang=[]
hdr = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'}
for i in item_list:
    print(i)
    url='https://search.shopping.naver.com/search/all.nhn?query={}&cat_id=&frm=NVSHATC'.format(i)
    #url2='https://search.naver.com/search.naver?where=post&sm=tab_jum&query={}'.format(i)
    #url3='https://search.naver.com/search.naver?where=article&sm=tab_jum&query={}'.format(i)
    url11='https://www.coupang.com/np/search?component=&q={}&channel=recent'.format(i)
    uurl='https://m.search.naver.com/search.naver?sm=mtp_hty.top&where=m&query={}'.format(i)
    oope=requests.get(uurl)
    hhtml=oope.text
    ssoup=bs(hhtml,'html.parser')
    
    
    tx=ssoup.findAll('h2',{'class':'api_title'}) 
    nnum=naver_(tx)
    
    

    reponse = requests.get(url11, headers = hdr)
    source = reponse.text

    soup11 = bs(source, 'html.parser')
    
    st=soup11.find('p',{'class':'hit-count'})
    try:
        coupang_num=int(st.findAll('strong')[1].text.replace(',',''))
    except:
        coupang_num=0
    
    
    
    ope=requests.get(url)
    #ope2=requests.get(url2)
    #ope3=requests.get(url3)
    html=ope.text
    #html2=ope2.text
    #html3=ope3.text
    soup=bs(html,'html.parser')
    #soup2=bs(html2,'html.parser')
    #soup3=bs(html3,'html.parser')
    
    t=soup.find('span',{'class':'subFilter_num__2x0jq'})
    #t2=soup2.find('span',{'class':'title_num'})
    #t3=soup3.find('span',{'class':'title_num'})
    
    try:
        pp=soup.find('div',{'class':'basicList_depth__2QIie'})
        ppp=list(pp.children)
        toto=''
        for j in range(len(ppp)):
            if j!=len(ppp)-1:
                toto+=ppp[j].text+'->'
            else:
                toto+=ppp[j].text
        category.append(toto)
    except:
        category.append('None')
    #blog.append(t2.text.split()[-1])
    #cafe.append(t3.text.split()[-1])
    rank.append(nnum)
    coupang.append(coupang_num)
    if t != None:
        store_num.append(int(t.text.replace(',','')))
        
    else:
        store_num.append(0)    
    


# In[77]:


data['검색수합계']=data['PC월간검색수']+data['모바일월간검색수']
data['스토어숫자']=store_num
data['쿠팡상품수']=coupang
#data['블로그숫자']=blog
#data['카페숫자']=cafe
data['사이트 내 네이버쇼핑순위']=rank
data['카테고리']=category

# In[78]:


s=True
while s:
    try:
        driver.close()
        current_tab=driver.window_handles[-1]
        driver.switch_to_window(window_name=current_tab)
        time.sleep(1)
        
    except:
        s=False


# In[79]:


data['네이버경쟁률']=data['스토어숫자']/(data['PC월간검색수']+data['모바일월간검색수'])
data['쿠팡경쟁률']=data['쿠팡상품수']/(data['PC월간검색수']+data['모바일월간검색수'])

columns_title=['연관키워드','PC월간검색수','모바일월간검색수', '검색수합계' ,'PC월평균클릭수','모바일월평균클릭수','PC월평균클릭률','모바일월평균클릭률' ,'경쟁정도' ,'월평균노출광고수' ,'스토어숫자' ,'네이버경쟁률','쿠팡상품수' ,'쿠팡경쟁률' ,'사이트 내 네이버쇼핑순위' ,'카테고리']
data.reindex(columns=columns_title)

# In[80]:


now=datetime.datetime.now()


# In[98]:


time=('%02d%02d%02d-%02d%02d%02d' %(int(str(now.year)[2:]),now.month,now.day,now.hour,now.minute,now.second))


# In[100]:


if d==1:
    data.to_csv(time+'_'+a+','+str(minimum)+'~'+str(maximum)+'.csv',index=None,encoding='utf-8-sig')
else:
    data.to_csv(time+'_'+a+','+'조건없음'+'.csv',index=None,encoding='utf-8-sig')

