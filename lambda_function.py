{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww37900\viewh20740\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import json\
import os \
import requests\
import psycopg2\
import boto3   \
from datetime import datetime\
\
def lambda_handler(event, context):\
    # API key from environment variable\
    api_key = os.environ['WEATHER_API_KEY']\
    city = "London"\
    \
    # Get weather data\
    url = f"http://api.openweathermap.org/data/2.5/weather?q=\{city\}&appid=\{api_key\}&units=standard"\
    response = requests.get(url)\
    data = response.json()\
    \
    # Extract relevant information \
    timestamp = datetime.now().isoformat()\
    temperature = data['main']['temp']\
    humidity = data['main']['humidity']\
    description = data['weather'][0]['description']\
    \
    # Store raw data in S3\
    s3 = boto3.client('s3')\
    bucket_name = os.environ['S3_BUCKET_NAME']\
    s3.put_object(\
        Bucket=bucket_name,\
        Key=f"raw_data/\{timestamp\}.json",\
        Body=json.dumps(data)\
    )\
    \
    # Store processed data in RDS\
    conn = psycopg2.connect(\
        host=os.environ['DB_HOST'],\
        database=os.environ['DB_NAME'],\
        user=os.environ['DB_USER'],\
        password=os.environ['DB_PASSWORD']\
    )\
    cursor = conn.cursor()\
    insert_query = """\
    INSERT INTO weather_data (timestamp, city, temperature, humidity, description)\
    VALUES (%s, %s, %s, %s, %s)\
    """\
    \
    cursor.execute(insert_query, (timestamp, city, temperature, humidity, description))\
    conn.commit()\
    cursor.close()\
    conn.close()\
    \
    return \{\
        'statusCode': 200,\
        'body': json.dumps('Weather data processed successfully!')\
    \}\
    \
    }