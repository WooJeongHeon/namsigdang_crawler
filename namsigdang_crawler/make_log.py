import requests
import datetime

from data.account.slack_key import token, channel
from data_path import path_all_log, path_error_log


def slack_msg(msg):
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": "Bearer " + token},
                  data={"channel": channel, "text": msg})


class WriteLogs:

    def __init__(self, log_path, logText):
        self.log_path = log_path
        self.logText = logText

    def __str__(self):
        return f"{datetime.datetime.now()}: {self.logText}"

    def write_to_file(self):
        logfile = open(self.log_path, 'a')
        logfile.writelines(str(datetime.datetime.now()) + ": " + self.logText + "\n")
        logfile.close()


def write_log(log_text, log_file=path_all_log):
    write_logs = WriteLogs(log_file, log_text)
    print(write_logs)
    write_logs.write_to_file()
