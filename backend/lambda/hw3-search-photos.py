import json
import logging
import random
import string
import boto3

from botocore.vendored import requests

# import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

PHOTOS_ELASTICSEARCH_BASE_URL = 'https://vpc-hw3-photos-ajqy7hye46hwf5v5bzzeo3pgmi.us-east-1.es.amazonaws.com/photos/_search'


def generate_id():
    c = string.ascii_lowercase + string.digits
    return ''.join(random.choice(c) for i in range(5))


def extract_item(item):
    bucket = item["_source"]["bucket"]
    object_key = item["_source"]["objectKey"]
    labels = item["_source"]
    image_url = "https://{:s}.s3.amazonaws.com/{:s}".format(bucket, object_key)
    return {
        "url": image_url,
        "labels": labels
    }


def search_images(query):
    # es stuf
    try:

        url = PHOTOS_ELASTICSEARCH_BASE_URL + "?q=%s" % query
        es_response = requests.get(url).json()

        logger.debug(json.dumps(es_response, indent=2))
        if "hits" not in es_response and "hits" not in es_response["hits"]:
            return {
                'statusCode': 400,
                'body': "Bad Request"
            }
        return {
            'statusCode': 200,
            'body': json.dumps({"results": list(map(extract_item, es_response["hits"]["hits"]))})
        }
    except Exception as e:
        logger.error(str(e))
        return {
            'statusCode': 400,
            'body': "Bad Request"
        }


def lambda_handler(event, context):
    response = dict()
    response["headers"] = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT",
        "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    }
    try:
        if event["httpMethod"].upper() == "OPTIONS":
            response['statusCode'] = 200

            return response

        logger.info("event:")
        logger.info(json.dumps(event, indent=2))

        query = event["queryStringParameters"]['q']
        
        # 
        lex = boto3.client('lex-runtime')
        user_id = generate_id()
        # logger.info(user_id)
        bot_name = 'SearchBot'
        lex_response = lex.post_text(
            botName=bot_name,
            botAlias=bot_name,
            userId=user_id,
            inputText=query
        )
        logger.info("lex_response:")
        logger.info(lex_response)
        
        keywords = []
        for key, val in lex_response['slots'].items():
            keywords.append(val)
        keyword = keywords[0]

        logger.info(keyword)

        response.update(search_images(keyword))
    except Exception as e:
        logger.error(e)
        response['statusCode'] = 400
        response["body"] = "Bad Request"
    return response
