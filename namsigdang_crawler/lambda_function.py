from crawler_main import run
import json


def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(run("aws_lambda_docker"))
    }


if __name__ == "__main__":
    print(lambda_handler("", ""))
