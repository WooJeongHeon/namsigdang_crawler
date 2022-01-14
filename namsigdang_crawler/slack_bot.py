import requests
from data.account.slack_key import token, channel


def slack_msg(msg):
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": "Bearer " + token},
                  data={"channel": channel, "text": msg})
