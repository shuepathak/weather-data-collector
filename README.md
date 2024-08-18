
## Project Overview

The Weather Data Collector is a serverless application built on AWS that automatically fetches, processes, and stores weather data. It utilizes AWS Lambda for computation,retrieves data from a public weather API, stores raw data in Amazon S3, and saves processed data in an Amazon RDS PostgreSQL database.\

## Architecture\

The project uses the following AWS services:
1. AWS Lambda
2. Amazon S3
3. Amazon RDS (PostgreSQL)
4. Amazon CloudWatch Events (for scheduling)

## Components

### 1. Lambda Function

The core of the application is an AWS Lambda function written in Python. This function:
- Fetches weather data from OpenWeatherMap API
- Processes the raw data
- Stores raw data in S3
- Inserts processed data into RDS

### 2. S3 Bucket

An S3 bucket named `weatherbetatest` is used to store the raw JSON data received from the API.

### 3. RDS PostgreSQL Database

An RDS instance hosts a PostgreSQL database named `weather-database-1`. It stores the processed weather data in a structured format.

## Setup Instructions

1. Create an AWS account if you don't have one.
2. Set up the AWS CLI on your local machine.
3. Create an S3 bucket named `weatherbetatest`.
4. Set up an Amazon RDS PostgreSQL instance named `weather-database-1`.
5. Create an AWS Lambda function and deploy the provided Python code.
6. Configure environment variables in the Lambda function:
   - WEATHER_API_KEY
   - S3_BUCKET_NAME
   - DB_HOST
   - DB_NAME
   - DB_USER
   - DB_PASSWORD
7. Set up necessary IAM permissions for the Lambda function to access S3 and RDS.
8. Create a CloudWatch Events rule to trigger the Lambda function daily.

## Database Schema

The `weather_data` table in the PostgreSQL database has the following schema:

```sql
CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    city VARCHAR(100),
    temperature FLOAT,
    humidity FLOAT,
    description TEXT
);}
