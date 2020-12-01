import datetime
import json
import logging

import boto3
from botocore.vendored import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def generate_label_list(photo, bucket):
    # logger.debug("Ready to go to reko.")
    # logger.debug(photo)
    # logger.debug(bucket)
    client = boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
                                    MaxLabels=10)
    # logger.info("reko response:")
    # logger.info(json.dumps(response,indent=2))
    label_list = []
    for label in response['Labels']:
        label_list.append(label['Name'].lower())
    return label_list


def lambda_handler(event, context):
    # TODO implement
    # logger.info("event:")
    # logger.info(json.dumps(event,indent=2))

    records = event["Records"]
    for record in records:
        s3 = record["s3"]
        photo = s3["object"]["key"]
        bucket = s3["bucket"]["name"]
    label_list = generate_label_list(photo, bucket)
    # logger.info("labels:")
    logger.info(label_list)

    url = 'https://vpc-hw3-photos-ajqy7hye46hwf5v5bzzeo3pgmi.us-east-1.es.amazonaws.com/photos/_doc'
    header = {"Content-Type": "application/json"}

    params = {
        "objectKey": photo,
        "bucket": bucket,
        "createdTimestamp": str(datetime.datetime.now()),
        "labels": label_list
    }
    logger.info("body:")
    logger.info(json.dumps(params, indent=2))

    response_es = requests.post(url, data=json.dumps(params), headers=header)
    logger.info("response data:" + json.dumps(response_es.json()))

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
