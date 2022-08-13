from namsigdang_crawler_v2 import namsigdang_crawler
import json


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(namsigdang_crawler())
    }
