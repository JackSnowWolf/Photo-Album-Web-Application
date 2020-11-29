import json
import logging
import random
import string

import boto3
from botocore.vendored import requests

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def generate_id():
    c = string.ascii_lowercase + string.digits
    return ''.join(random.choice(c) for i in range(5))


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

        # logger.info("event:")
        # logger.info(json.dumps(event,indent=2))
        message = event["queryStringParameters"]['q']
        lex = boto3.client('lex-runtime')

        user_id = generate_id()
        # logger.info(user_id)
        bot_name = 'SearchBot'
        lex_response = lex.post_text(
            botName=bot_name,
            botAlias=bot_name,
            userId=user_id,
            inputText=message
        )
        # logger.info(lex_response)

        keywords = []
        for key, val in lex_response['slots'].items():
            keywords.append(val)
        keyword = keywords[0]

        # logger.info(keyword)

        # es stuf
        url = 'https://vpc-hw3-photos-ajqy7hye46hwf5v5bzzeo3pgmi.us-east-1.es.amazonaws.com/photos/_search'
        header = {"Content-Type": "application/json"}
        query = {
            "size": 1000,
            "query": {"match": {"labels": keyword}}
        }
        es_response = requests.post(url, data=json.dumps(query), headers=header)
        logger.info(es_response)

        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT",
                "Access-Control-Allow-Headers": "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
            },
            'body': json.dumps({"files": es_response})
            # 'body': json.dumps('Hello from Lambda!')
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
