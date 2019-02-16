import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# 종목 메인 url 생성(모바일)
# code : 종목코드
def get_item_main_url_mobile(code):
    return 'https://m.stock.naver.com/item/main.nhn#/stocks/{code}/total'.format(code=code)


# 종합 항목 맵핑
def get_tot_eng_nm(x):
    return {'전일'         :'price_day_before',
            '시가'         :'price_start',
            '고가'         :'price_hight',
            '저가'         :'price_row',
            '거래량'       :'transaction_volumn',
            '대금'         :'transaction_payment',
            '시총'         :'market_capitalization',
            '외인소진율'   :'foreign_exhaustion_rate',
            '52주 최고'    :'52week_high',
            '52주 최저'    :'52week_row',
            'PER(FnGuide)' :'per_fnguide',
            'EPS(FnGuide)' :'eps_fnguide',
            'PER(KRX)'     :'per_krx',
            'EPS(KRX)'     :'eps_krx',
            '추정PER'      :'estimated_per',
            '추정EPS'      :'estimated_eps',
            'PBR(FnGuide)' :'pbr_fnguide',
            'BPS(FnGuide)' :'pbs_fnguide',
            '배당수익률'   :'dividend_yield_ratio',
            '주당배당금'   :'dividend',
            '주주총회일'   :'day_of_stockholders_meeting',
            '전자투표제Tip':'vote'}.get(x, 'undefinded')


# 종합(모바일)
def get_total_info(soup):
    # 종합(모바일) 리스트 선택
    total_info = soup.select('ul.total_lst > li')

    # 반복문 인덱스
    number = 0
    # 반복문을 통한 "네이버 증권 모바일 페이지"의 "종합" 정보 파싱
    for li in total_info:
        # 항목 명칭
        div = li.select('div')
        # 항목 명칭 문자열 변경, 앞뒤 공백 제거
        div_text = div[0].text.strip()

        # 항목 값
        span = li.select('span')
        # 항목 값 문자열 변경, 앞뒤 공백제거, ',' 제거
        span_text = span[0].text.strip().replace(',', '')

        # (20:주주총회일, 21:전자투표제Tip) 제외
        if number < 20:
            # 숫자(소수점 포함) 추출
            span_number = re.search(r"\d+(\.\d+)?", span_text)

            # 숫자(소수점 포함) 존재할 경우
            if span_number is not None:
                # 추출된 값 할당(문자열)
                span_text = span_number.group(0)
        elif number == 20:
            # 20:주주총회일 YYYYMMDD 형태로 변경 ('.' 제거)
            span_text = span_text.replace('.', '')

        print(number, '\t/ ', div_text, ' / ', span_text, ' / ', get_tot_eng_nm(div_text))

        # 인덱스 증가
        number += 1


# 039130 하나투어
# 종목 메인 request 객체 생성
req = requests.get('https://m.stock.naver.com/api/html/item/getOverallInfo.nhn?code=039130')

# html소스를 soup = BeautifulSoup 객체로 변환
soup = BeautifulSoup(req.text, 'html.parser')

investment_info = {}

# 종합(모바일) 정보 크롤링
get_total_info(soup)


