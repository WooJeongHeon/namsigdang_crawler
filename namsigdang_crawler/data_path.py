from my_date import my_date, day_of_the_week, today_date

project_path = '.'
# project_path = '/home/ubuntu/namsigdang-server/namsigdang_crawler' # 절대경로 기입

path_dir_data = project_path + '/data'
path_dir_data_log = path_dir_data + '/log'
path_dir_data_all_log = path_dir_data + '/log/all_log'
path_all_log = path_dir_data + '/log/all_log/' + my_date()[0:4] + '_year/' + my_date()[
                                                                             5:7] + '_month/all_log(' + my_date() + ').txt'
path_error_log = path_dir_data + '/log/error_log.txt'
path_change_DB_log = path_dir_data + '/log/change_DB_log.txt'

path_dir_data_crawling_menu = path_dir_data + '/crawling_menu'
path_this_week_menu_csv = path_dir_data + '/crawling_menu/this_week_menu.csv'
path_backup_menu_csv = path_dir_data + '/crawling_menu/backup_menu.csv'
path_all_menu_txt = path_dir_data + '/crawling_menu/all_menu.txt'
path_all_menu_dat = path_dir_data + '/crawling_menu/all_menu.dat'

path_dir_data_account = path_dir_data + '/account'
path_account = path_dir_data + '/account/account.txt'
