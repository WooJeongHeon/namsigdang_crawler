# -*- encoding: utf-8 -*-

from cgi import parse_qs
import json
import pickle


def application(environ, start_response):
    path = environ['PATH_INFO'].split('/')
    request_body_size = int(environ.get('CONTENT_LENGTH', '0'))
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)
    # name = d.get('name', [''])[0]
    # age = d.get('age', [''])[0]
    print('method: %s' % environ['REQUEST_METHOD'])
    print('path: %s' % repr(path))

    f = open("dic.dat", "rb")
    dic_list = pickle.load(f)
    f.close()

    # response = {'name': name, 'age': age, 2018072301 : "test"}
    response = {"code": "success", "msg": "error none",

                # -------------------- 2018년 5월 은평관 식단 --------------------
                "eu20180501a": "허니버터브래드,생크림/쨈,우유,양배추콘슬로우"

                }

    response.append(dic_list)

    response_body = json.dumps(response)
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]
