import requests
from bs4 import BeautifulSoup
import pandas as pd


# 종목 메인 url 생성(모바일)
# code : 종목코드
def get_item_main_url_mobile(code):
    return 'https://m.stock.naver.com/item/main.nhn#/stocks/{code}/total'.format(code=code)


# 종합 항목 맵핑
def f(x):
    return {'전일': '111',
            '시가': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'a': '1',
            'b': '2'}.get(x, '3')


# 종합(모바일)
def get_total_info(soup):
    # 종합(모바일)
    total_info = soup.select('ul.total_lst > li')

    print("종합(모바일)--------------------------------------------------------")

    number = 0
    for li in total_info:
        div = li.select('div')
        span = li.select('span')
        print(number, '\t/ ', div[0].text, ' / ', span[0].text.strip())



        number += 1



# 039130 하나투어
# 종목 메인 request 객체 생성
req = requests.get('https://m.stock.naver.com/api/html/item/getOverallInfo.nhn?code=039130')

# BeautifulSoup으로 html소스를 python객체로 변환
soup = BeautifulSoup(req.text, 'html.parser')

investment_info = {}

# 종합(모바일)
get_total_info(soup)


