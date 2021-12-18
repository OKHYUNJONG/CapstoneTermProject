import os
import sys
import urllib.request
import pandas as pd
from ast import literal_eval
from bs4 import BeautifulSoup

class PapagoTranslate:
    def __init__(self,client_id,client_secret,csv_path,ko_column_name):
        self.client_id = client_id
        self.client_secret = client_secret
        self.csv_path = csv_path
        self.ko_column_name = ko_column_name
        self.df = pd.read_csv(self.csv_path)
        self.count = 0
    def ko2eng(self):
        new_df = pd.DataFrame()
        for i, text in enumerate(self.df[self.ko_column_name]):
            encText = urllib.parse.quote(str(text))
            data = "source=ko&target=en&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",self.client_id[self.count])
            request.add_header("X-Naver-Client-Secret",self.client_secret[self.count])
            try:
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
                    response_body = response_body.decode('utf-8')
                    soup = BeautifulSoup(response_body,"lxml")
                    body = soup.get_text()
                    for j in range(len(body)):
                        if body[j] == ":":
                            if body[j-2] == "t" and body[j-3] == "x":
                                slice_index = j+2
                                j += 2
                                while body[j] != '\"':
                                    j += 1
                                slice_index2 = j
                                break 
                    body = body[slice_index:slice_index2]
                    print(i,body)
                    new_df.loc[i,"index"] = i
                    new_df.loc[i,"번역"] = body
                    
                else:
                    print("Error Code:" + rescode)

            except urllib.error.HTTPError:
                self.count +=1

                data = "source=ko&target=en&text=" + encText
                url = "https://openapi.naver.com/v1/papago/n2mt"
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id",self.client_id[self.count])
                request.add_header("X-Naver-Client-Secret",self.client_secret[self.count])
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
                    response_body = response_body.decode('utf-8')
                    soup = BeautifulSoup(response_body,"lxml")
                    body = soup.get_text()
                    for j in range(len(body)):
                        if body[j] == ":":
                            if body[j-2] == "t" and body[j-3] == "x":
                                slice_index = j+2
                                j += 2
                                while body[j] != '\"':
                                    j += 1
                                slice_index2 = j
                                break 
                    body = body[slice_index:slice_index2]
                    print(i,body)
                    new_df.loc[i,"index"] = i
                    new_df.loc[i,"번역"] = body
                    
                else:
                    print("Error Code:" + rescode)
        print("done!")
        return new_df

    def eng2ko(self):
        new_df = pd.DataFrame()
        for i, text in enumerate(self.df[self.ko_column_name]):
            encText = urllib.parse.quote(str(text))
            data = "source=en&target=ko&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id",self.client_id[self.count])
            request.add_header("X-Naver-Client-Secret",self.client_secret[self.count])
            try:
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
                    response_body = response_body.decode('utf-8')
                    soup = BeautifulSoup(response_body,"lxml")
                    body = soup.get_text()
                    for j in range(len(body)):
                        if body[j] == ":":
                            if body[j-2] == "t" and body[j-3] == "x":
                                slice_index = j+2
                                j += 2
                                while body[j] != '\"':
                                    j += 1
                                slice_index2 = j
                                break 
                    body = body[slice_index:slice_index2]
                    print(i,body)
                    new_df.loc[i,"index"] = i
                    new_df.loc[i,"번역"] = body
                    
                else:
                    print("Error Code:" + rescode)

            except urllib.error.HTTPError:
                self.count +=1
                if self.count == 10:
                    print("api 사용량 초과 : 현재까지의 번역 기록을 저장합니다")
                    return new_df
                data = "source=ko&target=en&text=" + encText
                url = "https://openapi.naver.com/v1/papago/n2mt"
                
                request = urllib.request.Request(url)
                request.add_header("X-Naver-Client-Id",self.client_id[self.count])
                request.add_header("X-Naver-Client-Secret",self.client_secret[self.count])
                response = urllib.request.urlopen(request, data=data.encode("utf-8"))
                rescode = response.getcode()
                if(rescode==200):
                    response_body = response.read()
                    response_body = response_body.decode('utf-8')
                    soup = BeautifulSoup(response_body,"lxml")
                    body = soup.get_text()
                    for j in range(len(body)):
                        if body[j] == ":":
                            if body[j-2] == "t" and body[j-3] == "x":
                                slice_index = j+2
                                j += 2
                                while body[j] != '\"':
                                    j += 1
                                slice_index2 = j
                                break 
                    body = body[slice_index:slice_index2]
                    print(i,body)
                    new_df.loc[i,"index"] = i
                    new_df.loc[i,"번역"] = body
                    
                else:
                    print("Error Code:" + rescode)
        print("done!")
        return new_df




