# -*- encoding: utf-8 -*-

from pytz import timezone
from datetime import datetime
import pickle

from cgi import parse_qs
import json


def application(environ, start_response):
    path = environ['PATH_INFO'].split('/')
    request_body_size = int(environ.get('CONTENT_LENGTH', '0'))
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)

    campus = d.get('campus', [''])[0]  # "en"
    date = d.get('date', [''])[0]  # 20180809
    meal = d.get('meal', [''])[0]  # "a"

    contentType = d.get('contentType', [''])[0]  # eatok, eatno, eatthinking,  grade, comment
    change = d.get('change', [''])[0]  # plus1, minus1, 1~5
    commentContent = d.get('commentContent', [''])[0]  # "(닉네임): 이렇게 댓글 달릴거임. test1   "
    admin = d.get('admin', [''])[0]  # "wjh"

    print('method: %s' % environ['REQUEST_METHOD'])
    print('path: %s' % repr(path))

    # =========================================================================================================
    # =========================================================================================================
    # =========================================================================================================

    # 함수 (2개) ---------------------------------------

    # 에러메시지 함수
    def make_log_error(error_code):
        log = korea_time + code + "     " + error_code  # 여기에 파라미터 정보 전부 추가하기
        f = open(absolute_path + "log_error" + korea_month + ".txt", "a")
        f.write(log + "\n")
        f = open(absolute_path + "log_all" + korea_month + ".txt", "a")
        f.write(log + "\n")

        # 테스트용 프린트
        # print("에러 발생 테스트용 프린트: ", error_code)

    # 개별, all 로그 출력
    def make_log_success(def_message, def_log_name):

        # 로그 내용
        log = korea_time + code + "     " + def_message

        # 개별 로그 출력
        f = open(absolute_path + def_log_name + korea_month + ".txt", "a")
        f.write(log + "\n")

        # all 로그 출력
        f = open(absolute_path + "log_all" + korea_month + ".txt", "a")
        f.write(log + "\n")

    # 변수 선언------------------------------------------------
    code = campus + str(date) + meal
    absolute_path = "/var/www/namsigdang/"

    fmt = "(%Y-%m-%d %H:%M:%S %Z%z)     "
    UTC = datetime.now(timezone('UTC'))
    KST = datetime.now(timezone('Asia/Seoul'))

    UTC_time = UTC.strftime(fmt)
    korea_time = KST.strftime(fmt)
    korea_month = KST.strftime("_%Y.%m")

    # 딕션어리 선언------------------------------------------------

    dic_all_menu = {}  # 메뉴 데이터
    dic_notice = {}  # 공지사항 데이터

    dic_eat_ok = {}  # 먹어요
    dic_eat_no = {}  # 안먹어요
    dic_eat_thinking = {}  # 고민중
    dic_menu_grade_sum = {}  # 별점 sum
    dic_menu_grade_num = {}  # 별점 투표 수
    dic_menu_grade_avg = {}  # 별점 평균
    dic_comment = {}  # 댓글

    dic_today_output = {}  # 조회날짜 메뉴, 먹어요, 안먹어요 수, 고민중 수, 별점, 댓글

    # 메인 프로그램------------------------------------------------

    if (campus == "en" or campus == "do") and 20000000 < int(date) < 25000000 and (
            meal == "a" or meal == "b" or meal == "c"):
        make_log_success("식단을 조회했습니다", "log_menu")

        # "전체 메뉴" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_all_menu.dat', 'rb')
        dic_all_menu = pickle.load(f)
        f.close

        # "공지사항" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_notice.dat', 'rb')
        dic_notice = pickle.load(f)
        f.close

        # "먹어요" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_eat_ok.dat', 'rb')
        dic_eat_ok = pickle.load(f)
        f.close

        # "안먹어요" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_eat_no.dat', 'rb')
        dic_eat_no = pickle.load(f)
        f.close()

        # "고민중" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_eat_thinking.dat', 'rb')
        dic_eat_thinking = pickle.load(f)
        f.close()

        # "별점 sum" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_menu_grade_sum.dat', 'rb')
        dic_menu_grade_sum = pickle.load(f)
        f.close()

        # "별점 투표자 수" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_menu_grade_num.dat', 'rb')
        dic_menu_grade_num = pickle.load(f)
        f.close()

        # "별점 평균" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_menu_grade_avg.dat', 'rb')
        dic_menu_grade_avg = pickle.load(f)
        f.close

        # "댓글" 데이터파일로 딕션어리 초기화
        f = open(absolute_path + 'data_comment.dat', 'rb')
        dic_comment = pickle.load(f)
        f.close

        if not (code in dic_all_menu):
            dic_all_menu.update({code: "식단 정보를 찾을 수 없습니다."})
            make_log_success("식단 등록 X (식단 정보를 찾을 수 없습니다. 출력)", "log_menu")

        if not (code in dic_eat_ok):
            dic_eat_ok.update({code: 0})
            make_log_success("먹어요 수를 0으로 초기화 했습니다. (첫 조회)", "log_eat_ok")

        if not (code in dic_eat_no):
            dic_eat_no.update({code: 0})
            make_log_success("안먹어요 수를 0으로 초기화 했습니다. (첫 조회)", "log_eat_no")

        if not (code in dic_eat_thinking):
            dic_eat_thinking.update({code: 0})
            make_log_success("고민중 수를 0으로 초기화 했습니다. (첫 조회)", "log_eat_thinking")

        if not (code in dic_menu_grade_sum):
            dic_menu_grade_sum.update({code: 0})
            make_log_success("별점 sum을 0으로 초기화 했습니다. (첫 조회)", "log_menu_grade")

        if not (code in dic_menu_grade_num):
            dic_menu_grade_num.update({code: 0})
            make_log_success("별점 투표자 수를 0으로 초기화 했습니다. (첫 조회)", "log_menu_grade")

        if not (code in dic_menu_grade_avg):
            dic_menu_grade_avg.update({code: 0})
            make_log_success("별점 수 평균을 0으로 초기화 했습니다. (첫 조회)", "log_menu_grade")

        if not (code in dic_comment):
            dic_comment.update({code: ""})
            make_log_success("댓글을 빈 문자열로 초기화 하였습니다. (첫 조회)", "log_comment")

        # 먹어요 변경
        if contentType == "eatok":
            if change == "plus1":  # 먹어요 +1일 경우
                dic_eat_ok[code] += 1
                make_log_success("먹어요를 +1 하였습니다.     누적 먹어요: " + str(dic_eat_ok[code]), "log_eat_ok")

            elif change == "minus1":  # 먹어요 -1일 경우
                dic_eat_ok[code] -= 1
                make_log_success("먹어요를 -1 하였습니다.     누적 먹어요: " + str(dic_eat_ok[code]), "log_eat_ok")

            else:
                make_log_error("정헌에러코드7c936")

            f = open(absolute_path + 'data_eat_ok.dat', 'wb')
            pickle.dump(dic_eat_ok, f)
            f.close

        # 안먹어요 변경
        elif contentType == "eatno":
            if change == "plus1":  # 안먹어요 +1일 경우
                dic_eat_no[code] += 1
                make_log_success("안먹어요를 +1 하였습니다.     누적 안먹어요: " + str(dic_eat_no[code]), "log_eat_no")

            elif change == "minus1":  # 안먹어요 -1일 경우
                dic_eat_no[code] -= 1
                make_log_success("안먹어요를 -1 하였습니다.     누적 안먹어요: " + str(dic_eat_no[code]), "log_eat_no")

            else:
                make_log_error("정헌에러코드74g8s")

            f = open(absolute_path + 'data_eat_no.dat', 'wb')
            pickle.dump(dic_eat_no, f)
            f.close



        # 고민중 변경
        elif contentType == "eatthinking":
            if change == "plus1":  # 고민중 +1일 경우
                dic_eat_thinking[code] += 1
                make_log_success("고민중을 +1 하였습니다.     누적 고민중: " + str(dic_eat_thinking[code]), "log_eat_thinking")

            elif change == "minus1":  # 고민중 -1일 경우
                dic_eat_thinking[code] -= 1
                make_log_success("고민중을 -1 하였습니다.     누적 고민중: " + str(dic_eat_thinking[code]), "log_eat_thinking")

            else:
                make_log_error("정헌에러코드2h79")

            f = open(absolute_path + 'data_eat_thinking.dat', 'wb')
            pickle.dump(dic_eat_thinking, f)
            f.close




        # 별점 변경
        elif contentType == "grade":
            if change == 1 or change == 2 or change == 3 or change == 4 or change == 5:
                dic_menu_grade_sum[code] += change
                dic_menu_grade_num[code] += 1
                dic_menu_grade_avg[code] = dic_menu_grade_sum[code] / dic_menu_grade_num[code]
                dic_menu_grade_avg[code] = round(dic_menu_grade_avg[code], 2)

                text_grade_sum = "누적 별점 sum: " + str(dic_menu_grade_sum)
                text_grade_num = ", 누적 별점 투표자 수: " + str(dic_menu_grade_num)
                text_grade_avg = ", 누적 별점 평균: " + str(dic_menu_grade_avg)

                make_log_success(
                    "별점을 +" + str(change) + " 하였습니다.     " + text_grade_sum + text_grade_num + text_grade_avg,
                    "log_menu_grade")

                f = open(absolute_path + 'data_menu_grade_sum.dat', 'wb')
                pickle.dump(dic_menu_grade_sum, f)
                f.close

                f = open(absolute_path + 'data_menu_grade_num.dat', 'wb')
                pickle.dump(dic_menu_grade_num, f)
                f.close

                f = open(absolute_path + 'data_menu_grade_avg.dat', 'wb')
                pickle.dump(dic_menu_grade_avg, f)
                f.close



            else:
                make_log_error("정헌에러코드f37s")


        # 댓글
        elif contentType == "comment":
            if commentContent == "":
                make_log_error("정헌에러코드t492")
            else:
                dic_comment[code] = commentContent + "\n" + dic_comment[code]  # 앞줄에 입력한 댓글 추가

                f = open(absolute_path + 'data_comment.dat', 'wb')
                pickle.dump(dic_comment, f)
                f.close

                make_log_success("댓글을 추가 하였습니다.     추가한 댓글: " + commentContent, "log_comment")





        else:
            make_log_error("정헌에러코드9v3g")

        # dic_today_output 딕션어리 처음 선언. (조회날짜 메뉴, 먹어요, 안먹어요 수, 고민중 수, 별점, 댓글)

        dic_today_output["menu"] = dic_all_menu[code]

        dic_today_output["eat_ok"] = dic_eat_ok[code]
        dic_today_output["eat_no"] = dic_eat_no[code]
        dic_today_output["eat_thinking"] = dic_eat_thinking[code]

        dic_today_output["grade_avg"] = dic_menu_grade_avg[code]

        dic_today_output["comment"] = dic_comment[code]

        dic_today_output["notice"] = dic_notice[1]







    else:
        make_log_error("정헌에러코드29m73")

    # < 테스트 프린트 >

    # print("data_all_menu.dat 테스트: ", dic_all_menu)
    # print("data_eat_ok.dat 테스트: ", dic_eat_ok)
    # print("data_eat_no.dat 테스트: ", dic_eat_no)
    # print("data_eat_thinking.dat 테스트: ", dic_eat_thinking)
    # print("\ndata_menu_grade_sum.dat 테스트: ", dic_menu_grade_sum)
    # print("data_menu_grade_num.dat 테스트: ", dic_menu_grade_num)
    # print("data_menu_grade_avg.dat 테스트: ", dic_menu_grade_avg)
    # print("\ndata_comment.dat 테스트: ", dic_comment)
    # print("\ndata_comment.dat (현재 코드 value) 테스트: ", dic_comment[code])
    # print("data_notice.dat 테스트: ", dic_notice)
    # print("data_today_output.dat 테스트: ", dic_today_output)

    # =========================================================================================================
    # =========================================================================================================
    # =========================================================================================================

    response_body = json.dumps(dic_today_output)

    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]
