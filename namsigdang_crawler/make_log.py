import requests
import datetime

from data.account.slack_key import token, channel
from data_path import path_all_log, path_error_log


def slack_msg(msg):
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": "Bearer " + token},
                  data={"channel": channel, "text": msg})


def write_logs(logText):
    print(str(datetime.datetime.now()) + ": " + logText)

    logfile = open(path_all_log, 'a')
    logfile.writelines(str(datetime.datetime.now()) + ": " + logText + "\n")
    logfile.close()


def write_error_log(logText):
    logfile = open(path_error_log, 'a')
    logfile.writelines(str(datetime.datetime.now()) + ": " + logText + "\n")
    logfile.close()
