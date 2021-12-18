import base64
import json
from google.cloud import bigquery


def hello_pubsub(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    fmkorea_to_bq(pubsub_message)

def fmkorea_to_bq(fmkorea):
 client = bigquery.Client()
 dataset_ref = client.dataset('writtens')
 table_ref = dataset_ref.table('posts')
 table = client.get_table(table_ref)
 fmkorea_dict = json.loads(fmkorea)
 rows_to_insert = [(fmkorea_dict['id'], 
 fmkorea_dict['title'], 
 fmkorea_dict['category'],
 fmkorea_dict['product_name'],
 fmkorea_dict['price'],
 fmkorea_dict['shopping_fee'],
 fmkorea_dict['hotdeal_place'],
 fmkorea_dict['link'],
 fmkorea_dict['img_url'], 
 fmkorea_dict['shop_url'], 
 fmkorea_dict['text'],
 fmkorea_dict['date'],
 fmkorea_dict['time'])]


 error = client.insert_rows(table, rows_to_insert)
 print(error)


