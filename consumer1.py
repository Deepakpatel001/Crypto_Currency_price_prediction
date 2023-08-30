import pandas as pd
import mysql.connector
from kafka import KafkaConsumer
from json import dumps, loads
import json
from s3fs import S3FileSystem
import boto3
import botocore
import os


def create_dir_if_not_exist(prnt_dir, dr):
    path = os.path.join(prnt_dir, dr)

    if os.path.isdir(path):
        print("Directory '% s' already exists" % dr)
    else:
        os.mkdir(path)
        print("Directory '% s' created" % dr)
    return


def mysql_connect(d_host, d_user, d_password, d_database):
    mydb = mysql.connector.connect(
        host=d_host,
        user=d_user,
        password=d_password,
        database=d_database
    )
    return mydb


def mysql_cursor(my_database):
    my_cursor = my_database.cursor()
    return my_cursor


def insert_data_into_mysql_table(file_path, my_cursor, my_database):
    data = pd.read_csv(file_path)

    df = pd.DataFrame(data, columns=["id", "date", "open", "high", "low", "close", "volume", "volumeNotional", "tradesDone"])
    data_tuples = list(df.itertuples(index=False, name=None))
    insert_query = "INSERT INTO {} (date,open,high,low,close,volume,volumeNotional,tradesDone) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)".format('items')
    my_cursor.executemany(insert_query, data_tuples)
    my_database.commit()
    return


def close_mysql_conn(my_cursor, my_database):
    my_cursor.close()
    my_database.close()
    return


def retrieve_from_kakfa_and_store_in_db(topic_name, server_add, bucket_name, directory_path, my_cursor, my_database):
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=[server_add + ':9092'],
        value_deserializer=lambda x: loads(x.decode('utf-8')))

    for c in consumer:
        csv_file_obj_key = str(c.value['csv_file_obj_key'])
        # print("csv_file_obj_key",csv_file_obj_key)
        filepath = download_file_from_s3_and_return_filepath(bucket_name, csv_file_obj_key, directory_path)
        insert_data_into_mysql_table(filepath, my_cursor, my_database)
        # print(csv_file_obj_key)

    return


def download_file_from_s3_and_return_filepath(bucket_name, csv_file_obj_key, directory_path):
    s3_connection = boto3.resource(
        service_name="s3",
        region_name='ap-south-1',
        aws_access_key_id='AKIA45Y4MG2ZGT3D4PVG',
        aws_secret_access_key='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')

    bucket = s3_connection.Bucket(bucket_name)

    file = directory_path + csv_file_obj_key + ".csv"

    with open(file, 'wb') as data:
        bucket.download_fileobj(csv_file_obj_key, data)

    return file


db_host = "crypto-currency-prediction.cdctacolhwtf.ap-south-1.rds.amazonaws.com"
db_user = "root"
db_password = "password123"
db_database = "db_crypto_currency_prediction"
s3_bucket_name = "crypto-currency-storage-buck"
kafka_topic_name = "crypto-currency-topic"
kafka_server_ip_add = "13.232.255.147"
parent_dir = "C:\\Users\\Usha\\PycharmProjects\\Dashborad\\"
download_directory = "downloadDir\\"
download_directory_path = parent_dir + download_directory

my_db = mysql_connect(db_host, db_user, db_password, db_database)
my_cur = mysql_cursor(my_db)

create_dir_if_not_exist(parent_dir, download_directory)

retrieve_from_kakfa_and_store_in_db(kafka_topic_name, kafka_server_ip_add, s3_bucket_name, download_directory_path, my_cur, my_db)
