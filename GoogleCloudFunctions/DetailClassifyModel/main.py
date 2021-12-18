import datetime
import pandas as pd
from google.cloud import storage
import gcsfs
import ppomppumodels
import mysql.connector
from mysql.connector.constants import ClientFlag

config = {
    'user': 'root',
    'password': '내 비밀번호',
    'host': '내 sql IP 주소',
    'client_flags': [ClientFlag.SSL],
}

config['database'] = 'hotdealpost' 
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()

client = storage.Client()

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    utcnow= datetime.datetime.utcnow()
    time_gap= datetime.timedelta(hours=9)
    n= utcnow+ time_gap
    #df = pd.read_csv("gs://hotdealpost_rawdata/ppomppu_hotdeal/ymd={:04d}{:02d}{:02d}/time={:02d}{:02d}.csv".format(n.year, n.month, n.day, n.hour, n.minute-1))
    df = pd.read_csv("gs://hotdealpost_rawdata/ppomppu_hotdeal/ymd=20211115/time=1059.csv")
    df["label_x"] = ""
    df = df[["written_num","title","category","label_x",'price','shopping_fee','hotdeal_place','link','img_url','shop_url','text','date','time']]
    indexlist = []
    for i in range(len(df)):
      if df.loc[i,"category"].find('디지털') != -1:
          indexlist.append(i)
    df2 = df[df.category.str.contains('디지털')]


    pred = ppomppumodels.digit(df2)

    for i in range(len(indexlist)):
      df.loc[indexlist[i],'label_x'] = pred[i]

    print(df2)
    df2 = df2[["written_num","title","category","label_x",'price','shopping_fee','hotdeal_place','link','img_url','shop_url','text','written_time','date','time']]
    query = ("INSERT INTO posts (written_num,title,category,label_x,price,shopping_fee,hotdeal_place,link,img_url,shop_url,text,written_time,date,time) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    df2  = df2.fillna("")
    cursor.executemany(query, list(df2.to_records(index=False)))
    cnxn.commit() 

    return('finished')
