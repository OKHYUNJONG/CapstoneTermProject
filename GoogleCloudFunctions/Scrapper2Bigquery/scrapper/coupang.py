import hmac
import hashlib
import binascii
import os
import time
import requests
from bs4 import BeautifulSoup
import json


headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
REQUEST_METHOD = "POST"
DOMAIN = "https://api-gateway.coupang.com"
URL = "/v2/providers/affiliate_open_api/apis/openapi/v1/deeplink"


# Replace with your own ACCESS_KEY and SECRET_KEY
ACCESS_KEY = "53ec2472-bfde-44fb-8c61-c62a9f1b35c0"
SECRET_KEY = "ebbfd552402a20b27e7b3dc4a1c9dfa3f922c599"


def generateHmac(method, url, secretKey, accessKey):
    path, *query = url.split("?")
    os.environ["TZ"] = "GMT+0"
    datetime = time.strftime('%y%m%d')+'T'+time.strftime('%H%M%S')+'Z'
    message = datetime + method + path + (query[0] if query else "")

    signature = hmac.new(bytes(secretKey, "utf-8"),
                         message.encode("utf-8"),
                         hashlib.sha256).hexdigest()

    return "CEA algorithm=HmacSHA256, access-key={}, signed-date={}, signature={}".format(accessKey, datetime, signature)


def makeurl(shop_url):
    res = requests.get(shop_url,headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.content, "lxml")
    coupangpage = soup.find("meta", attrs = {"property":"og:url"})["content"]
    REQUEST = { "coupangUrls": [
        f"{coupangpage}"
    ]} 

    authorization = generateHmac(REQUEST_METHOD, URL, SECRET_KEY, ACCESS_KEY)
    url = "{}{}".format(DOMAIN, URL)
    resposne = requests.request(method=REQUEST_METHOD, url=url,
                                headers={
                                    "Authorization": authorization,
                                    "Content-Type": "application/json"
                                },
                                data=json.dumps(REQUEST)
                                )

    return resposne.json()["data"][0]["landingUrl"]
