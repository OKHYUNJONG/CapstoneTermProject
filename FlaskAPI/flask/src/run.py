import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage
from google.oauth2 import service_account
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import re
import time
import mysql.connector
from mysql.connector.constants import ClientFlag

app = Flask(__name__)
CORS(app)


config = {
    'user': 'root',
    'password': '우리의 비밀번호',
    'host': '우리 아이피',
    'client_flags': [ClientFlag.SSL],
}


config['database'] = 'hotdealpost'  
cnxn = mysql.connector.connect(**config)
cursor = cnxn.cursor()

def make_query_posts_catrgory(querydate,category):
    if querydate[4] == '0':
        month =  querydate[5]
    else:
        month =  querydate[4:6]
    if querydate[6] == '0':
        day = querydate[7]
    else:
        day = querydate[6:8]
    date = f"{querydate[0:4]}-{month}-{day}"
    cursor.execute(f"""
    SELECT written_num,title,category,price,hotdeal_place,img_url,date,time
    FROM `posts` 
    WHERE date = "{date}" and category = "{category}" 
    ORDER BY date DESC
    """)
    query_job = cursor
    return query_job 

def make_query_posts_term_catrgory(querydate,category):
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
    cursor.execute(f"""
    SELECT written_num,title,category,price,hotdeal_place,img_url,date,time 
    FROM `posts` 
    WHERE date >= "{date}" and date <= "{date2}" and category = "{category}" 
    ORDER BY date DESC
    """)
    query_job = cursor
    return query_job 

def make_query_posts_catrgory_detail(querydate,category,detail):
    if querydate[4] == '0':
        month =  querydate[5]
    else:
        month =  querydate[4:6]
    if querydate[6] == '0':
        day = querydate[7]
    else:
        day = querydate[6:8]
    date = f"{querydate[0:4]}-{month}-{day}"
    cursor.execute(f"""
    SELECT written_num,title,category,price,hotdeal_place,img_url,date,time
    FROM `posts` 
    WHERE date = "{date}" and category = "{category}" and label_x = "{detail}"
    ORDER BY date DESC
    """)
    query_job = cursor
    return query_job 

def make_query_posts_term_catrgory_detail(querydate,category,detail):
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
    cursor.execute(f"""
    SELECT written_num,title,category,price,hotdeal_place,img_url,date,time 
    FROM `posts` 
    WHERE date >= "{date}" and date <= "{date2}" and category = "{category}" and label_x = "{detail}"
    ORDER BY date DESC
    """)
    query_job = cursor
    return query_job 

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
    cursor.execute(f"""
    SELECT written_num,title,category,price,hotdeal_place,img_url,date,time
    FROM `posts` 
    WHERE date = "{date}"
    ORDER BY date DESC
    """)
    query_job = cursor
    return query_job 

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
    cursor.execute(f"""
    SELECT written_num,title,category,price,hotdeal_place,img_url,date,time 
    FROM `posts` 
    WHERE date >= "{date}" and date <= "{date2}"
    ORDER BY date DESC
    """)
    query_job = cursor
    return query_job 

def make_query_post(id):
    cursor.execute(f"""
    SELECT * 
    FROM `posts` 
    WHERE written_num = "{id}"
    """)
    query_job = cursor
    return query_job 

#example input: /posts/20210531/먹거리 처럼 0 포함

@app.route('/posts/<querydate>/<category>')
def get_posts_category(querydate,category):
    start_time = time.time()
    result = []
    query_job = make_query_posts_catrgory(querydate,category)
    for row in query_job:   

        temp = {
            'id':row[0],
            'title':row[1],
            'category':row[2],
            'price':row[3],
            'hotdeal_place':row[4],
            'img_url':row[5],
            'date':row[6],
            'time':row[7],
            }
        result.append(temp)
    end_time = time.time()
    print(f'response after {end_time - start_time}')
    return jsonify(result)

@app.route('/termposts/<querydate>/<category>')
def get_termposts_category(querydate,category):
    start_time = time.time()
    result = []
    query_job = make_query_posts_term_catrgory(querydate,category)
    for row in query_job:   

        temp = {
            'id':row[0],
            'title':row[1],
            'category':row[2],
            'price':row[3],
            'hotdeal_place':row[4],
            'img_url':row[5],
            'date':row[6],
            'time':row[7],
            }
        result.append(temp)
    end_time = time.time()
    print(f'response after {end_time - start_time}')
    return jsonify(result)

@app.route('/posts/<querydate>/<category>/<detail>')
def get_posts_category_detail(querydate,category,detail):
    start_time = time.time()
    result = []
    query_job = make_query_posts_catrgory_detail(querydate,category,detail)
    for row in query_job:   

        temp = {
            'id':row[0],
            'title':row[1],
            'category':row[2],
            'price':row[3],
            'hotdeal_place':row[4],
            'img_url':row[5],
            'date':row[6],
            'time':row[7],
            }
        result.append(temp)
    end_time = time.time()
    print(f'response after {end_time - start_time}')
    return jsonify(result)

#example input: /termposts/2021053120210603 처럼 0 포함
@app.route('/termposts/<querydate>/<category>/<detail>')
def get_termposts_category_detail(querydate,category,detail):
    start_time = time.time()
    result = []
    query_job = make_query_posts_term_catrgory_detail(querydate,category,detail)
    for row in query_job:   

        temp = {
            'id':row[0],
            'title':row[1],
            'category':row[2],
            'price':row[3],
            'hotdeal_place':row[4],
            'img_url':row[5],
            'date':row[6],
            'time':row[7],
            }
        result.append(temp)
    end_time = time.time()
    print(f'response after {end_time - start_time}')
    return jsonify(result)

#example input: /posts/20210531 처럼 0 포함

@app.route('/posts/<querydate>')
def get_posts(querydate):
    start_time = time.time()
    result = []
    query_job = make_query_posts(querydate)
    for row in query_job:   

        temp = {
            'id':row[0],
            'title':row[1],
            'category':row[2],
            'price':row[3],
            'hotdeal_place':row[4],
            'img_url':row[5],
            'date':row[6],
            'time':row[7],
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
    query_job = make_query_posts_term(querydate)
    for row in query_job:   

        temp = {
            'id':row[0],
            'title':row[1],
            'category':row[2],
            'price':row[3],
            'hotdeal_place':row[4],
            'img_url':row[5],
            'date':row[6],
            'time':row[7],
            }
        result.append(temp)
    end_time = time.time()
    print(f'response after {end_time - start_time}')
    return jsonify(result)
    


@app.route('/post/<id>')
def get_post(id):
    result = []
    query_job = make_query_post(id)
    for row in query_job:   
        nums = row[10].count('\n')
        texts = re.split('\n', row['text'])

        temp = {
            'id':row[0],
            'title':row[1],
            'category':row[2],
            'label_x':row[3],
            'price': row[4],
            'shopping_fee':row[5],
            'hotdeal_place':row[6],
            'link':row[7],
            'img_url':row[8],
            'shop_url':row[9],
            'text':texts,
            'written_time':row[11],
            'date':row[12],
            'time':row[13]    
            }
        result.append(temp)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
