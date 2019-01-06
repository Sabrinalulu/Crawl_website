from selenium import webdriver
driver = webdriver.Chrome('/Users/sabrinalulu/jupyterNote/chromedriver')
driver.get('https://www.ncbi.nlm.nih.gov/pubmed')

# use selector to find element ex.search box
q = driver.find_element_by_name('term')
# type in what you want to search 
q.send_keys('food allergy')

# execute
from selenium.webdriver.common.keys import Keys
q.send_keys(Keys.RETURN)

from pyquery import PyQuery as pq
from lxml import etree
response = driver.page_source
# the string changes to the byte
html = bytes(bytearray(response, encoding='utf-8'))
html = etree.HTML(html)
global doc
doc = pq(html)

def changeToHtml(target):
    response = target
    html = bytes(bytearray(response, encoding='utf-8'))
    html = etree.HTML(html)
    return html
    
import urllib.request
dataset=[]
doc.make_links_absolute(base_url="https://www.ncbi.nlm.nih.gov")
for eachTxt in doc("#maincontent > div > div:nth-child(5) > div > div.rslt > p > a").items():
#     print(eachTxt)
    start = eachTxt.attr("href")
    driver.get(start)
    firstpage = changeToHtml(driver.page_source)
    second = pq(firstpage)
#     print(second)
    for eachDetail in second("#maincontent > div > div.rprt_all > div > div.abstr > div > p").items():
        print(eachDetail.text())
        
def nextPage(i):
# //*[@id="pageno2"]
# 參考資料：https://tw.saowen.com/a/0e7d504386f0b54707680427eecb38f7dad7f8d637847b97c0e670820b61c016
# browser.execute_script("document.getElementById(\'" + ordinal + "\').value=\'" + parameter + "\';")
    driver.execute_script("document.getElementById('pageno2').value=\'" + i + "\';")
    q = driver.find_element_by_id('pageno2')
    q.send_keys(Keys.RETURN)
    
driver.get("https://www.ncbi.nlm.nih.gov/pubmed/?term=food+allergy")
user_input = input('Give me a page number: ')
nextPage(user_input)
nextpage = driver.page_source
# print(driver.page_source)
nextpagesource = changeToHtml(nextpage)
doc1 = pq(nextpagesource)
# 製作成連結
doc1.make_links_absolute(base_url="https://www.ncbi.nlm.nih.gov")
for eachTxt in doc1("#maincontent > div > div:nth-child(5) > div > div.rslt > p > a").items():
    # 找到下一個網址和base結合就是nextStart ex.https://www.ncbi.nlm.nih.gov/pubmed/30582491
    nextstart = eachTxt.attr("href")
    driver.get(nextstart)
    firstpage = changeToHtml(driver.page_source)
    nextsecond = pq(firstpage)
    for eachDetail in nextsecond("#maincontent > div > div.rprt_all > div > div.abstr > div > p").items():
        print(eachDetail.text())

