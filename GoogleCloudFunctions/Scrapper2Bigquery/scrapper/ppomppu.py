import requests
from bs4 import BeautifulSoup
import time
import os
import threading
import time
import re
import json 
import datetime
from google.cloud import pubsub_v1
from google.oauth2 import service_account
import sys
from flask import escape
import coupang as cp


def crawling_ppomppu():
  utcnow= datetime.datetime.utcnow()
  time_gap= datetime.timedelta(hours=9)
  n= utcnow+ time_gap
  now_time = f"{n.hour}:{n.minute}"
  now_date = f"{n.year}-{n.month}-{n.day}"
  now_minute = n.hour * 60 + n.minute


  crawling = True
  page=1
  while crawling == True:
    url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page="+str(page)+"&divpage=68"
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    writtens = soup.find_all("tr",attrs = {"class":[re.compile("^list0"),re.compile("^list1")]})
    for i in range(len(writtens)):
      written_time = writtens[i].find("nobr", attrs = {"class":"eng list_vspace"}).get_text().strip()
      time2min = int(written_time[0:2])*60 + int(written_time[3:5])
      if '/' in written_time or abs(now_minute - time2min)>=60:
        crawling = False
        break
      written_time = written_time[:5]
      category = writtens[i].find("span", attrs = {"style":re.compile("^color:#999;font-size:11px;")}).get_text()

      tmp = writtens[i].find_all("td", attrs = {"align":"left"})
      if tmp[1].get_text().strip() == "HOT 게시글에서 제외된 글입니다.":
        continue              
      tmp_title = tmp[1].get_text().strip()[:-2].strip()
      maketitle= False
      k = 0
      hotdeal_place = ""
      for i in range(len(tmp_title)):
        if tmp_title[i] == "]":
          k = i
          hotdeal_place = tmp_title[1:k]
        if tmp_title[i] == "(" and i>k:
          maketitle= True
          title = tmp_title[k+1:i]
          break
          
      havemid = False 
      start = 0 

      shopping_fee = ''
      for i in range(len(tmp_title)-1,0,-1):
        if tmp_title[i] == ")":
          start = i
        if tmp_title[i] == "/" and i<start:
          mid = i
          havemid = True
          shopping_fee = tmp_title[i+1:start]
        if tmp_title[i] == "(" and i<start:
          if havemid == True:
            price = tmp_title[i+1:mid]
          else:
            price = tmp_title[i+1:start]
      if maketitle == False:
        title = tmp_title[k+1::]
        price =""
        shopping_fee = ""
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

      if hotdeal_place == "쿠팡" and shop_url != "판매종료로 url없음":
        try:
          shop_url = cp.makeurl(shop_url)
        except:
          print(id,"쿠팡파트너스 변환 실패")
      if textstring == '' or shop_url == 'http://본문':
          textstring = '커뮤니티 글 참조'
      category = category.replace("[","")
      category = category.replace("]","")
      print(written_num)
      block = json.dumps({'id': written_num,
              'title': title,
              'category' : category,
              'product_name': title,
              'price':price,
              'shopping_fee':shopping_fee,
              'hotdeal_place':hotdeal_place,
              'link': link,
              'img_url' :img_url,
              'shop_url':shop_url,
              'text':textstring,
              'date':now_date,
              'time':now_time}, default=str)
      client.publish(topic_path, data=block.encode('utf-8'))

    page+=1    
