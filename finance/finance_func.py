import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import sqlite3
import time


# 종목 메인 url 생성(모바일)
# code : 종목코드
def get_item_main_url_mobile(code):
    return 'https://m.stock.naver.com/item/main.nhn#/stocks/{code}/total'.format(code=code)


# 종합 항목 맵핑
# ? Placeholder 사용하면서 사용하지 않음
# Named Placeholder를 사용하게되면 다시 사용할지도...
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
def get_total_info(stock_cd, soup):
    # 종합(모바일) 리스트 선택
    total_info = soup.select('ul.total_lst > li')

    ret = []
    #ret_obj = {'stock_cd': stock_cd}

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

        # (5:대금, 6:시총)
        if number == 5 or number == 6:
            pass
        # (8:52주 최고, 9:52주 최저)
        elif number == 8 or number == 9:
            if div[0].find('span') is not None:
                div_text = div[0].text.replace(div[0].find('span').text, '').strip()
                span_text = span[1].text.replace(span[1].find('span').text, '').replace(',', '')

        # (20:주주총회일, 21:전자투표제Tip)
        elif number == 20 or  number == 21:
            # 20:주주총회일 YYYYMMDD 형태로 변경 ('.' 제거)
            span_text = span_text.replace('.', '')

        else:
            # 숫자(소수점 포함) 추출
            #span_text = re.sub(r"[^0123456789\.]", "", span_text)
            # 숫자(소수점 포함) 추출
            span_number = re.search(r"-?\d+(\.\d+)?", span_text)

            # 숫자(소수점 포함) 존재할 경우
            if span_number is not None:
                # 추출된 값 할당(문자열)
                span_text = span_number.group(0)

        #print(number, '\t/ ', div_text, ' / ', span_text, ' / ', get_tot_eng_nm(div_text))
        #print(number, '\t/ ', div_text, ' / ', span_text)

        ret.append(span_text)
        #ret_obj[get_tot_eng_nm(div_text)] = span_text

        # 반복문 인덱스 증가
        number += 1

    ret.append(stock_cd)
    return ret

# SQLite DB 연결
conn = sqlite3.connect("test.db")

# Connection 으로부터 Cursor 생성
cur = conn.cursor()

cur.execute('SELECT stock_cd FROM TBL_TOTAL_INF')

stock_list = cur.fetchall()

sql = """UPDATE TBL_TOTAL_INF SET
[price_day_before] = ?,
[price_start] = ?,
[price_hight] = ?,
[price_row] = ?,
[transaction_volumn] = ?,
[transaction_payment] = ?,
[market_capitalization] = ?,
[foreign_exhaustion_rate] = ?,
[52week_high] = ?,
[52week_row] = ?,
[per_fnguide] = ?,
[eps_fnguide] = ?,
[per_krx] = ?,
[eps_krx] = ?,
[estimated_per] = ?,
[estimated_eps] = ?,
[pbr_fnguide] = ?,
[pbs_fnguide] = ?,
[dividend_yield_ratio] = ?,
[dividend] = ?,
[day_of_stockholders_meeting] = ?,
[vote] = ?
WHERE stock_cd = ?"""

# 시작시간
start_time = time.time()
print('start_time = ', start_time)

investment_info = []

stock_list_tot = len(stock_list)

number = 1

for stock in stock_list:
    # 종목 메인 request 객체 생성
    req = requests.get('https://m.stock.naver.com/api/html/item/getOverallInfo.nhn?code=' + stock[0])

    # html소스를 soup = BeautifulSoup 객체로 변환
    soup = BeautifulSoup(req.text, 'html.parser')

    # 종합(모바일) 정보 크롤링
    row = get_total_info(stock[0], soup)

    investment_info.append(row)

    #cur.execute(sql, row)

    print(number, '/', stock_list_tot)
    #print(number, '/', stock_list_tot, '/', stock[0], row)

    # 반복문 인덱스 증가
    number += 1
    '''
    if number == 10:
        break;
    '''
cur.executemany(sql, investment_info)

conn.commit()
# print(investment_info)
print("종료 --- seconds ---", int((time.time() - start_time)), '초')

cur.close()
conn.close()

