import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from datetime import *
import json


# error 로그 출력
def json_request_error(e):
    print('{0}: {1}'.format(e, datetime.now()), file=sys.stderr)

# success, error에 함수를 등록해주면 그 함수를 실행시키겠다는 의미
def json_request(url = '',  encoding = 'utf-8',
                success = None,
                error = json_request_error):
    try:
        req = Request(url)     # request 객체 생성
        res = urlopen(req)     # URL에 연결하여 response 객체 반환
        if res.getcode() == 200:
            res_body = res.read().decode(encoding)  # json string
            # print(res_body, type(res_body))
            res_json = json.loads(res_body)         # python 자료형인 Dictionary로 반환
             # print(json_result, type(json_result))

            if callable(success) is False:
                return res_json
            success(res_json)

    except Exception as e:
        callable(error) and error('%s %s' % (str(e), url))


BASE_URL_FB_API = 'https://graph.facebook.com/v11.0'
ACCESS_TOKEN = '' #Access_Token


# 여러 파라미터에 대하여, url을 생성
def fb_generate_url(base = BASE_URL_FB_API, node = '', **param):
    return '%s/%s?%s' % (base, node, urlencode(param))

def fb_name_to_id(pagename):
    url = fb_generate_url(node = pagename, access_token = ACCESS_TOKEN)
    # print(url)
    json_result = json_request(url)
    print(json_result)                # {'name': 'JTBC 뉴스', 'id': '240263402699918'}
    return json_result.get('id')


# 게시글 가져오기 - 크롤러는 최종적으로 이 함수를 사용한다.
# 인자로 페이스북 페이지명과 게시글 일자 기간을 넘겨준다.
#def fb_fetch_post(pagename, since, until):
def fb_fetch_post(pagename):
    # URL 생성 시, 여러 파라미터를 전달
    url = fb_generate_url(
        # node = fb_name_to_id( pagename ) + '/posts',
        node = 'oembed_page',
        # fields = 'id, message, link, name, type, shares, created_time,\
        #         reactions.limit(0).summary(true),\
        #         comments.limit(0).summary(true)',
        fields = 'id, name',
        # since = since,  # 시작 날짜
        # until = until,  # 끝 날짜
        # limit = 30,     # 개수
        access_token = ACCESS_TOKEN
    )
    # print(url)

    json_result = json_request(url)
    return json_result

# posts = fb_fetch_post('me', '2021-06-01', '2021-06-30')
posts = fb_fetch_post('me')
print(posts)
