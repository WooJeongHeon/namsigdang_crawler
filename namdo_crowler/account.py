import datetime
import os

class Account:
    def account_load(self):
        path_account = 'Data\\account.txt'
        path_log = 'Data\\log.txt'
        try:
            if os.path.exists(path_account):
                pass
            else:
                print("계정 파일이 없어 새로 생성합니다.")
                accountfile = open(path_account, 'w')
                accountfile.writelines(input("ID를 입력하세요: "))
                accountfile.writelines("\n")
                accountfile.writelines(input("PW를 입력하세요: "))
                accountfile.close()
            file = open(path_account, 'r')
            reader = file.readlines()
            account_list = []
            for data in reader:
                account_list.append(data.replace('\n', ''))
            return account_list
        except Exception as error:
            logfile = open(path_log, 'a')
            print(str(datetime.datetime.now()) + ": " + error)
            logfile.writelines(str(datetime.datetime.now()) + ": " + error + "\n")
            logfile.close()

if __name__ == "__main__":
    acc = Account()
    acc.account_load()