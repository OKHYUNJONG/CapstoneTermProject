import requests
from bs4 import BeautifulSoup
import time
import os
import threading
import time
import re
import json 
import datetime
import sys
from flask import escape
import csv
from google.cloud import storage
import pandas as pd
import gcsfs
client = storage.Client()



def crawling_fmkorea():
    arr = []
    #현재 시각
    utcnow= datetime.datetime.utcnow()
    time_gap= datetime.timedelta(hours=9)
    n= utcnow+ time_gap
    now_time = f"{n.hour}:{n.minute}"
    now_date = f"{n.year}-{n.month}-{n.day}"
    now_minute = n.hour * 60 + n.minute


    crawling = True
    page=1
    
    while crawling == True:
        url = "https://www.fmkorea.com/index.php?mid=hotdeal&page="+str(page)
        res = requests.get(url)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "lxml")

        writtens = soup.find_all("li", attrs = {"class":re.compile("^li li_")})

        for i in range(len(writtens)):
            time_ago = writtens[i].find("span", attrs = {"class":"regdate"}).get_text().strip()
            time2min = int(time_ago[0:2])*60 + int(time_ago[3:5])
            #1시간전 까지 출력
            if '.' in time_ago or abs(now_minute - time2min)>=10:
                crawling = False
                df = pd.DataFrame(arr, columns=['written_num','title','category','title','price','shopping_fee','hotdeal_place','link','img_url','shop_url','text','written_time'])
                df.to_csv("gs://hotdealpost_rawdata/fmkorea_hotdeal/ymd={:04d}{:02d}{:02d}/time={:02d}{:02d}.csv".format(n.year, n.month, n.day, n.hour, n.minute)) 
                break

            written = writtens[i].find("h3", attrs = {"class":"title"})

            hotdeal_info = writtens[i].find("div", attrs = {"class":"hotdeal_info"})
            #글 제목
            title = written.get_text().strip()
            for j in range(len(title)):
                if title[j] == '[':
                    k = j
            title = title[:k]
            #글 링크
            link = 'https://www.fmkorea.com'+written.a["href"]
            print(link)
            #글 인덱스(0_ -> fmkorea)
            written_num = "0_" + written.a["href"][85:]

            #쇼핑몰 이름
            if hotdeal_info:
                hotdeal_place = hotdeal_info.find("a", attrs = {"class":"strong"}).get_text().strip()
                
            
            #카테고리
            try:
                category = writtens[i].find("span", attrs = {"class":"category"}).a.get_text().strip()
                if category == "공지":
                    continue
            except:
                category = "no_category"

 
            image = writtens[i].find("img", attrs = {"class":"thumb"})

            if image:
                img = 'https:'+image["data-original"]
            else:
                img = "no_image"

            if img != "no_image":
                #글 링크 접속
                res = requests.get(link)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, "lxml")

                try:
                    img_url = soup.find("img", attrs = {"src":re.compile("^//image.fmkorea.com/files")})["src"]
                except:
                    img_url = soup.find("img", attrs = {"src":re.compile("^//image5jvqbd.fmkorea.com/")})["src"]
                #이미지 url
                img_url = "https:"+img_url

                #글 내용
                text = soup.find_all("div", attrs = {"class":re.compile("^document_")})[1].get_text(separator="\n", strip=True)

                #상품정보(상품url,제품명,가격,배송비)
                info = soup.find_all("div", attrs = {"class":re.compile("^xe_content")})
                shop_url = info[0].a["href"]
                product_name = info[2].get_text()
                price = info[3].get_text()
                shopping_fee = info[4].get_text()
                time.sleep(1)
            else:
                res = requests.get(link)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, "lxml")
                
                #이미지 url
                img_url = "no_image"
                #글 내용
                text = soup.find_all("div", attrs = {"class":re.compile("^document_")})[1].get_text(separator="\n", strip=True)

                #상품정보(상품url,제품명,가격,배송비)
                info = soup.find_all("div", attrs = {"class":re.compile("^xe_content")})
                shop_url = info[0].a["href"]
                product_name = info[2].get_text()
                price = info[3].get_text()
                shopping_fee = info[4].get_text()
                time.sleep(1)

            arr.append([written_num,title,category,product_name,price,shopping_fee,hotdeal_place,link,img_url,shop_url,textstring,written_time,now_date,now_time])

        # print(page)
        page+=1











