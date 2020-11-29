import json
import base64
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
    # TODO implement
    logger.debug("event: " + json.dumps(event))
    img_data = event['img']
    logger.info(img_data)
    image_name = event['name']
    img = base64.b64decode(img_data, validate=True)
    
    # our S# Bucket
    s3 = boto3.client('s3')
    bucket = 'b2photostore'
    
    img_path = '/tmp/'+image_name
    
    handler = open(img_path, "wb+")
    handler.write(img)
    handler.close()
    
    # upload the temp image to s3
    s3.upload_file(img_path, bucket, image_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
