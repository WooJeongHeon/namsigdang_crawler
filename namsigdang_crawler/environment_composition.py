import os

from data_path import path_dir_data, path_dir_data_log, path_dir_data_all_log, path_all_log, path_error_log, \
    path_change_DB_log, path_dir_data_crawling_menu, path_this_week_menu_csv, path_backup_menu_csv, path_all_menu_txt, \
    path_all_menu_dat, path_dir_data_account, path_account
from make_log import write_logs, write_error_log, slack_msg
from my_date import my_date, day_of_the_week, today_date


def make_path_dir(path_dir, bool):
    if not os.path.isdir(path_dir):
        os.mkdir(path_dir)

        if bool:
            write_logs(path_dir + "경로가 없어 새로 생성 했습니다.")


def make_path_file(path_file):
    if not os.path.exists(path_file):
        logfile = open(path_file, 'w')
        logfile.close()
        write_logs(path_file + "파일이 없어 새로 생성합니다.")


def create_env():
    make_path_dir(path_dir_data, False)  # 아직 로그 경로가 없어 로그생성 False
    make_path_dir(path_dir_data_log, False)
    make_path_dir(path_dir_data_all_log, False)
    make_path_dir(path_dir_data_all_log + my_date[0:4] + '_year', False)
    make_path_dir(path_dir_data_all_log + my_date[0:4] + '_year/' + my_date[5:7] + '_month', True)
    make_path_dir(path_dir_data_account, True)
    make_path_dir(path_dir_data_crawling_menu, True)

    make_path_file(path_all_log)
    make_path_file(path_error_log)
    make_path_file(path_change_DB_log)


def check_all_menu_dat():
    if os.path.exists(path_all_menu_dat):
        return True
    else:
        write_logs("\n\n\'" + path_all_menu_dat + "\' 파일이 없습니다.\n추가해 주세요!\n프로그램을 종료합니다.")
        return False


def check_account():
    if not os.path.exists(path_account):
        write_logs("계정 파일이 없어 새로 생성합니다.")
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

    my_id = account_list[0]
    my_pw = account_list[1]

    return my_id, my_pw
