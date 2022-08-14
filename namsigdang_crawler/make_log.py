import requests
import datetime

from data.account.slack_key import token, channel
from data_path import path_all_log, path_error_log


def slack_msg(msg):
    print(msg)
    requests.post("https://slack.com/api/chat.postMessage",
                  headers={"Authorization": "Bearer " + token},
                  data={"channel": channel, "text": msg})


class WriteLogs:

    def __init__(self, log_path, log_text):
        self.log_path = log_path
        self.log_text = log_text

    def __str__(self):
        return f"{datetime.datetime.now()}: {self.log_text}"

    def write_to_file(self):
        logfile = open(self.log_path, 'a')
        logfile.writelines(str(datetime.datetime.now()) + ": " + self.log_text + "\n")
        logfile.close()


def write_log(log_text, log_files=None, send_slack=False):
    if log_files is None:
        log_files = [path_all_log]

    n = 0
    for log_file in log_files:
        n += 1
        write_logs = WriteLogs(log_file, log_text)

        if n == 1:
            print(write_logs)
        write_logs.write_to_file()

    if send_slack:
        slack_msg(log_text)
