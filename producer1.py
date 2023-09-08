import csv
import requests
import json
import boto3
import boto
import os
from datetime import datetime
import secrets
import string
from kafka import KafkaProducer
from json import dumps

def create_dir_if_not_exist(prnt_dir, dir):
    path = os.path.join(prnt_dir, dir)

    if os.path.isdir(path):
        print("Directory '% s' already exists" % dir)
    else:
        os.mkdir(path)
        print("Directory '% s' created" % dir)
    return


def get_data_from_api_and_cvt_to_json(cpto_api_url):
    res = requests.get(cpto_api_url)
    print("res -> ",res)
    response = json.loads(res.text)
    print("response -> ", response)
    json_string = str(response)
    data = json.loads(json_string.replace("\'", "\""))
    print("json_data -> ", data)
    return data


def convert_json_to_csv_and_save_file(json_string, file_path):
    for obj in json_string:
        headers = obj['priceData'][0].keys()
        print("headers -> ",headers)
        with open(file_path, 'a') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(obj['priceData'])
    return


def upload_csv_to_aws_s3(file_path, bucket_name, obj_key):

    s3_connection = boto3.resource(
        service_name="s3",
        region_name='ap-south-1',
        aws_access_key_id='AKIA45Y4MG2ZGT3D4PVG',
        aws_secret_access_key='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')

    s3_connection.Bucket(bucket_name).upload_file(
        Filename=file_path,
        Key=obj_key)
    return

def generate_file_name():
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # print("Current date & time : ", current_datetime)
    str_current_datetime = str(current_datetime)
    file_name = str_current_datetime + ".csv"
    return file_name

def send_msg_to_kafka(topic_name, server_add, csv_file_obj_key):
    producer = KafkaProducer(bootstrap_servers=[server_add + ':9092'],
                             value_serializer=lambda x:
                             dumps(x).encode('utf-8'))

    producer.send(topic_name, value={'csv_file_obj_key': csv_file_obj_key})

# Historical intraday data
crypto_api_url = "https://api.tiingo.com/tiingo/crypto/prices?token=e71ab8b2817300d7a6b1b8dd1625d7924f37dc9c&tickers=btcusd&startDate=2023-08-26&endDate=2023-08-27&resampleFreq=60min"
parent_dir = "C:\\Users\\Usha\\PycharmProjects\\Dashborad\\"
upload_directory = "uploadDir\\"
csv_file_name = generate_file_name()
s3_bucket_name = "crypto-currency-storage-buck"
key_prefix = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(7))
obj_key = csv_file_name.replace(".csv", "") + '-' + key_prefix
kafka_topic_name = "crypto-currency-topic"
kafka_server_ip_add = "13.232.255.147"

create_dir_if_not_exist(parent_dir, upload_directory)

json_str = get_data_from_api_and_cvt_to_json(crypto_api_url)

upload_file_path = parent_dir + upload_directory + csv_file_name

convert_json_to_csv_and_save_file(json_str, upload_file_path)

upload_csv_to_aws_s3(upload_file_path, s3_bucket_name, obj_key)

# obj_key = "2023-08-27-12-58-04-6N056A3" #--- use only while testing
send_msg_to_kafka(kafka_topic_name, kafka_server_ip_add, obj_key)
