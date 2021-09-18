import requests
import json,os,sys
import pandas as pd 

import re

from selenium import webdriver
from bs4 import BeautifulSoup as bs
from datetime import datetime

def get_hunjang(url,pg):
    # webdriver 객체 생성
    driver = webdriver.Chrome('./chromedriver')
    
    # 페이지 접근
    driver.get(url)
    soup = bs(driver.page_source ,'html.parser')
    
    soup = soup.find(class_ = 's-adBn-wrap')#채용정보
    if pg <=1 :
        soup = soup.find_all(class_ = 'adRc-inner')[5] #1:스페셜, 2:포커스 3:플러스 4:리스트 5일반
    else:
        try:
            soup = soup.find_all(class_ = 'adRc-inner')[0] #두번째 페이지부터 바로
        except:
            print("이 페이지부턴 검색내용이 없음")
            return []

    table = soup.find('table', class_='retbl-col')
    rows = table.find_all('tr')
    
    datas_list=[]
    for idx,tr in enumerate(rows):
        result={}
        if idx>0:
            tds = tr.find_all('td')
            result['academy_name'] = tds[1].text.rstrip()
            result['title'] = tds[2].text.strip()
            result['local'] = tds[3].text.rstrip().split("\n")[1]
            result['subject']=tds[3].text.rstrip().split("\n")[2]
            
            result['start_date'] = tds[4].text
            result['end_date'] = tds[5].text
            datas_list.append(result)
                   
    return datas_list
    
def get_dataframe():
    
    df_fin = pd.DataFrame()

    for pg in range(1,31): #예상) 마지막페이지30, 그보다 적으면 중간에 break
        url = "https://www.hunjang.com/adopt/adopt_total_list.asp?schSubject=01&schSubject_name=%B1%B9%BE%EE&schSubject=02&schSubject_name=%BF%B5%BE%EE&schSubject=03&schSubject_name=%BC%F6%C7%D0&nPage="+str(pg)+"&nPageSize=20&sort_order=&textkey=&textword="
        data_list = get_hunjang(url,pg)
        if len(data_list) == 0:
            break

        df = pd.DataFrame(data_list,columns=['academy_name','title','local','subject','start_date','end_date'])
        df_fin = pd.concat([df_fin,df],axis=0,ignore_index=True)

    return df_fin

if __name__ == '__main__':

    today_date = datetime.today().strftime("%Y-%m-%d")
    df_fin = get_dataframe()
    #df.head()

    filename = today_date+'-hunjang_crawling.csv'  
    df_fin.to_csv('./AutoCrawling/'+filename,encoding='utf-8-sig')
    print("save csv!")

## 문제점 : 마지막페이작 계속 바뀜
