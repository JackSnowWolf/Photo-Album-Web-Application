import base64
import json
import logging

import boto3

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def lambda_handler(event, context):
    try:
        if event["httpMethod"].upper() == "OPTIONS":
            return {
                'statusCode': 200,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT",
                    "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
                },
                'body': ""
            }

        logger.debug("event: " + json.dumps(event))
        img_data = json.loads(event["body"])['img']
        logger.info(img_data)
        image_name = json.loads(event["body"])['name']
        img = base64.b64decode(img_data, validate=True)

        # our S# Bucket
        s3 = boto3.client('s3')
        bucket = 'hw3-b2-for-photos'

        img_path = '/tmp/' + image_name

        handler = open(img_path, "wb+")
        handler.write(img)
        handler.close()

        # upload the temp image to s3
        s3.upload_file(img_path, bucket, image_name)

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT",
                "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps('Hello from Lambda!')
        }
    except Exception as e:
        logger.error(e)
        return {
            'statusCode': 400,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT",
                "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': "Bad Request"
        }
