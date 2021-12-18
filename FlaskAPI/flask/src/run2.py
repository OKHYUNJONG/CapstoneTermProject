import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage
from google.oauth2 import service_account
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import re
import time

app = Flask(__name__)
CORS(app)

key_path = "hotmoa-315220-2d2bd7ec58f5.json"


credentials = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

bqclient = bigquery.Client(credentials=credentials, project='hotmoa-315220',)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)



def make_query_posts(querydate):
    if querydate[4] == '0':
        month =  querydate[5]
    else:
        month =  querydate[4:6]
    if querydate[6] == '0':
        day = querydate[7]
    else:
        day = querydate[6:8]
    date = f"{querydate[0:4]}-{month}-{day}"
    query = f"""
    SELECT id,title,category,hotdeal_place,img_url,date,time 
    FROM `hotmoa-315220.writtens.posts` 
    WHERE date = "{date}"
    ORDER BY CAST(SUBSTR(time, 0, INSTR(time, ':')-1) AS INT64  ) DESC
    """
    return query


def make_query_posts_term(querydate):
    if querydate[4] == '0':
        month =  querydate[5]
    else:
        month =  querydate[4:6]
    if querydate[6] == '0':
        day = querydate[7]
    else:
        day = querydate[6:8]

    if querydate[12] == '0':
        month2 =  querydate[13]
    else:
        month2 =  querydate[12:14]
    if querydate[14] == '0':
        day2 = querydate[15]
    else:
        day2 = querydate[14:16]


    date = f"{querydate[0:4]}-{month}-{day}"
    date2 = f"{querydate[0:4]}-{month2}-{day2}"
    query = f"""
    SELECT id,title,category,hotdeal_place,img_url,date,time 
    FROM `hotmoa-315220.writtens.posts` 
    WHERE date >= "{date}" and date <= "{date2}"
    ORDER BY CAST(SUBSTR(time, 0, INSTR(time, ':')-1) AS INT64  ) DESC
    """
    return query

def make_query_post(id):
    query = f"""
    SELECT * 
    FROM `hotmoa-315220.writtens.posts` 
    WHERE id = "{id}"
    """
    return query




#example input: /posts/20210531 처럼 0 포함

@app.route('/posts/<querydate>')
def get_posts(querydate):
    start_time = time.time()
    result = []
    query_job = bqclient.query(make_query_posts(querydate))
    for row in query_job:   

        temp = {
            'id':row['id'],
            'title':row['title'],
            'category':row['category'],
            'hotdeal_place':row['hotdeal_place'],
            'img_url':row['img_url'],
            'date':row['date'],
            'time':row['time']    
            }
        result.append(temp)
    end_time = time.time()
    print(f'response after {end_time - start_time}')
    return jsonify(result)

#example input: /termposts//2021053120210603 처럼 0 포함
@app.route('/termposts/<querydate>')
def get_termposts(querydate):
    start_time = time.time()
    result = []
    query_job = bqclient.query(make_query_posts_term(querydate))
    for row in query_job:   

        temp = {
            'id':row['id'],
            'title':row['title'],
            'category':row['category'],
            'hotdeal_place':row['hotdeal_place'],
            'img_url':row['img_url'],
            'date':row['date'],
            'time':row['time']    
            }
        result.append(temp)
    end_time = time.time()
    print(f'response after {end_time - start_time}')
    return jsonify(result)
    


@app.route('/post/<id>')
def get_post(id):
    result = []
    query_job = bqclient.query(make_query_post(id))
    for row in query_job:   
        nums = row['text'].count('\n')
        texts = re.split('\n', row['text'])

        temp = {
            'id':row['id'],
            'title':row['title'],
            'category':row['category'],
            'product_name':row['product_name'],
            'price': row['price'],
            'shopping_fee':row['shopping_fee'],
            'hotdeal_place':row['hotdeal_place'],
            'link':row['link'],
            'img_url':row['img_url'],
            'shop_url':row['shop_url'],
            'text':texts,
            'date':row['date'],
            'time':row['time']    
            }
        result.append(temp)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)