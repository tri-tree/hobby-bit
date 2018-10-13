
# coding: utf-8

# In[5]:

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import datetime # datetimeモジュールのインポート
import re

print "begin"

#browser = webdriver.Chrome(executable_path='C:\Users\akito\Anaconda2')
browser = webdriver.Chrome()

#プロキシ設定
#phantomjs_args = ['--cookie-file={}.format("cookie.txt")' ]
#phantomjs_args = [ '--proxy=kmt.proxy.nic.fujitsu.com:8080','--proxy-auth=mori.akito@jp.fujitsu.com:0987654321']

#browser open
#browser = webdriver.PhantomJS(service_args=phantomjs_args)    #プロキシ使う
#browser = webdriver.PhantomJS()
start = time.time()

#phantom起動
browser.get("https://www.mercari.com/jp/category/") # Load page
#browser.save_screenshot("test.png")
print "ok"


# In[ ]:

html_source = browser.page_source.encode('utf-8') # アクセスしたサイトのページソースを返す
html = BeautifulSoup(html_source,"html.parser")   #パーサー


# In[ ]:

''' #2017/4/25取得
sect1 = html.find_all("li",class_="pc-header-nav-parent") #parent
i = None; m= None; n = None;
for i in sect1:
    #sect1 = i.find_all("li",class_="pc-header-nav-parent")
    parent = i.find("h3").text.replace(u"\n","")
    parent_link = i.find("a").attrs["href"]
    sect2 = i.find_all("li",class_="pc-header-nav-child") #child
    for m in sect2:
        child = m.find("a").text
        child_link = m.find("a").attrs["href"]
        sect3 = m.find_all("li",class_="pc-header-nav-grand-child") #grand-child 
        print child
        for n in sect3:
            gchild = n.find("a").text
            gchild_link = n.find("a").attrs["href"]
            str = (u"%s,%s,%s,%s,%s,%s\n" % (parent,child,gchild,parent_link,child_link,gchild_link))

            with open("category_list.csv", 'a') as file: #出力ファイルオープン 追加書込み
                file.write(str.encode("utf-8"))
'''


# In[19]:

#ブランド一覧を取得
browser.get("https://www.mercari.com/jp/brand/") # Load page
#browser.save_screenshot("test.png")
print "ok"
html_source = browser.page_source.encode('utf-8') # アクセスしたサイトのページソースを返す
html = BeautifulSoup(html_source,"html.parser")   #パーサー


# In[22]:

#2017/4/25　取得
sect4 = html.find_all("div",class_="brand-list-initial-box-brand-list clearfix") #parent
i = None; m= None; n = None;
for i in sect4:
    sect5 = i.find_all("a")
    for m in sect5:
        brand = m.find("p").text.replace(u" ","")
        brand_link = m.attrs["href"] 

        str = (u"%s,%s\n" % (brand,brand_link))
        with open("brand_list.csv", 'a') as file: #出力ファイルオープン 追加書込み
            file.write(str.encode("utf-8"))
print "Done"

'''
sect1 = i.find_all("li",class_="pc-header-nav-parent")
parent = i.find("h3").text.replace(u"\n","")
parent_link = i.find("a").attrs["href"]
sect2 = i.find_all("li",class_="pc-header-nav-child") #child
for m in sect2:
    child = m.find("a").text
    child_link = m.find("a").attrs["href"]
    sect3 = m.find_all("li",class_="pc-header-nav-grand-child") #grand-child 
    print child
    for n in sect3:
        gchild = n.find("a").text
        gchild_link = n.find("a").attrs["href"]

'''

