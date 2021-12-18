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

def crawling_ppomppu():
  arr = []
  utcnow= datetime.datetime.utcnow()
  time_gap= datetime.timedelta(hours=9)
  n= utcnow+ time_gap
  now_time = f"{n.hour}:{n.minute}"
  now_date = f"{n.year}-{n.month}-{n.day}"
  now_minute = n.hour * 60 + n.minute
  written_num = 0

  crawling = True
  page=0
  while crawling == True:
    url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page="+str(page)+"&divpage=68"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    writtens = soup.find_all("tr",attrs = {"class":[re.compile("^list0"),re.compile("^list1")]})
    for i in range(len(writtens)):
      written_time = writtens[i].find("nobr", attrs = {"class":"eng list_vspace"}).get_text().strip()
      time2min = int(written_time[0:2])*60 + int(written_time[3:5])
      if '/' in written_time or abs(now_minute - time2min)>=10:
        crawling = False
        df = pd.DataFrame(arr, columns=['written_num','title','category','price','shopping_fee','hotdeal_place','link','img_url','shop_url','text','written_time','date','time'])
        df.to_csv("gs://hotdealpost_rawdata/ppomppu_hotdeal/ymd={:04d}{:02d}{:02d}/time={:02d}{:02d}.csv".format(n.year, n.month, n.day, n.hour, n.minute)) 
        break
      written_time = written_time[:8]
      category = writtens[i].find("span", attrs = {"style":re.compile("^color:#999;font-size:11px;")}).get_text()

      tmp = writtens[i].find_all("td", attrs = {"align":"left"})
      if tmp[1].get_text().strip() == "HOT 게시글에서 제외된 글입니다.":
        continue 

      tmp_title = tmp[1].get_text().strip()
      title = tmp_title.split("(")[0].split("]")[-1]
      if len(title) <2:
        title = tmp[1].get_text().strip()
        shopping_fee = "제목참조"
        price = '제목참조'
      else:
        tmp_title = tmp_title.split('>')[0]
        hotdeal_place = tmp_title.split(']')[0]
        if hotdeal_place[0] == '[':
          hotdeal_place = hotdeal_place[1:]

        s_price = tmp_title.split('(')[-1]
        if s_price[0] == '우' and s_price[1] == '주':
          s_price = tmp_title.split('(')[-2]
        if '/' in s_price:
          for i in range(len(s_price)):
            if s_price[i] == '/':
              k = i
            if s_price[i] == ')':
              l = i
              break
          price = s_price[:k]
          shopping_fee = s_price[k+1:l]
        else:
          price = s_price.split(')')[0]
          shopping_fee = ''


      title = title.strip()
      tmp_link = tmp[1].find("a")["href"]


      if tmp_link[:14] =="/zboard/zboard":
        tmp_link = "/zboard/view"+ tmp_link[14:]

      link = "https://www.ppomppu.co.kr/zboard/" + tmp_link
      index = ''
      for j in range(len(link)-1,0,-1):
        if link[j] == "=":
            break
        index += link[j]
      written_num ="2_" + index[::-1]

      image = tmp[1].find("img")["src"]
      if image != "//static.ppomppu.co.kr/www/img/noimage/noimage_60x50.jpg":
        res = requests.get(link)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'lxml')
        content = soup.find("td",attrs={"class":"board-contents"})
        shop_url = soup.find("div",attrs={"class":"wordfix"})
        try:
          shop_url = shop_url.find("a")["href"]
        except:
          shop_url = "판매종료로 url없음"
        if shop_url != "판매종료로 url없음":
          img_url = "https:" + soup.find("img")["src"]
          text = content.find_all("p")
          textstring = ''
          for i in text:
            textstring += i.get_text() + "\n"
        else:
          try:
            img_url = "https:" + soup.find("img")["src"]
          except:
            img_url = "no_image"
          textstring = " "

      else:
        img_url = "no_image"
        res = requests.get(link)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'lxml')
        content = soup.find("td",attrs={"class":"board-contents"})
        shop_url = soup.find("div",attrs={"class":"wordfix"})
        try:
          shop_url = shop_url.find("a")["href"]
        except:
          shop_url = "판매종료로 url없음"
        if shop_url != "판매종료로 url없음":
          text = content.find_all("p")
          textstring = ''
          for i in text:
            textstring += i.get_text() + "\n"
        else:
          textstring = " "


      if textstring == '' or shop_url == 'http://본문':
          textstring = '커뮤니티 글 참조'
      category = category.replace("[","")
      category = category.replace("]","")
      arr.append([written_num,title,category,price,shopping_fee,hotdeal_place,link,img_url,shop_url,textstring,written_time,now_date,now_time])
    page+=1
