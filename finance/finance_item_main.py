import requests
from bs4 import BeautifulSoup
import re
import sqlite3
import time


# 종목 메인 url 생성
# code : 종목코드
def get_item_main_url(code):
    return 'https://finance.naver.com/item/main.nhn?code={code}'.format(code=code)


# 기업개요 가져오기
# soup : BeautifulSoup 객체
def get_summary_info(soup):
    # 예외처리 : 파라미터 빈값
    if(soup is None):
        return ''

    # 기업개요 내용 조회
    summary_info_list = soup.select('#summary_info > p')

    # 리턴 문자열 변수 생성
    summary_info_text = ''

    # 존재 여부 확인
    if len(summary_info_list) > 0:

        # p 태그가 여러개인 경우 내용을 합친다
        for p in summary_info_list:
            summary_info_text += p.text

    return summary_info_text


# 튜플 : 전일, 시가, 고가, 저가, 거래량, 거래대금
list_title_1 = ('전일', '고가', '상한가', '거래량', '시가', '저가', '하한가', '거래대금')

# 튜플 : 투자정보 제목
list_title_2 = ('시가총액', '시가총액순위', '상장주식수', '액면가', '매매단위',
                '주총일', '전자투표',
                '외국인한도주식수(A)', '외국인보유주식수(B)', '외국인소진율(B/A)',
                '투자의견', '목표주가', '52주최고', '52주최저',
                'PER(FnGuide)', 'EPS(FnGuide)', 'PER(KRX)', 'EPS(KRX)',
                '추정PER', '추정EPS', 'PBR', 'BPS(FnGuide)',
                '배당수익률', '동일업종 PER', '동일업종 등락률')


# 투자정보
def get_investment_info(stock_cd, soup):
    print('stock_cd = ', stock_cd)
    stock_cd = '950170'
    #print('----------------------------- 전일, 시가, 고가, 저가, 거래량, 거래대금 -----------------------------')

    value_arr_1 = []

    # 전일, 시가, 고가, 저가, 거래량, 거래대금
    investment_info = soup.select('#chart_area > div.rate_info > table td > em')
    #print(investment_info)
    for idx, val in enumerate(investment_info):
        span = val.select('span:not(.blind)')
        value = ''
        for num in span:
            value += num.text

        value_arr_1.append(value.replace(',', ''))

    del value_arr_1[2]
    del value_arr_1[6-1]
    print('----------------------------- 투자정보 -----------------------------')

    value_arr_2 = []
    value_arr_title2 = []
    investment_info = soup.select('#tab_con1 > div > table tr')

    # 투자정보 파싱
    for idx, tr in enumerate(investment_info):
        # 투자정보 타이틀
        ths = tr.select('th')
        for i, th in enumerate(ths):
            # 타이틀
            th_title = th.text

            # 타이틀 tag 안에 div 태그 제거
            if len(th.select('div')) > 0:
                th_title = th.text.replace(th.select('div')[0].text, '')

            # 타이틀이 여러개일 경우 분리
            th_arr = th_title.replace('\n', '').replace('\t', '').replace(' ', '').split('l')

            # 음.... 배열의 길이가 1보다 클 경우에는
            # PER 등을 구분지어주기위해 다음 자리의 (FnGuide), (KRX), 추정 을 확인하여 앞에 붙여준다다

           if len(len(th_arr)) > 1:
                for j, text in enumerate(th_arr):
                    # if th_arr[j].find('')
                    value_arr_title2.append(th_arr[j])
            else:
                value_arr_title2.append(th_arr[0])

            '''
            # 타이틀 갯수만큼 배열에 추가
            for j, text in enumerate(th_arr):
                #if th_arr[j].find('')
                value_arr_title2.append(th_arr[j])
            '''
        # 투자정보 값
        tds = tr.select('td')
        for idx, td in enumerate(tds):
            td_arr = td.text.replace('\n', '').replace('\t', '').split('l')

            for j, text in enumerate(td_arr):
                value_arr_2.append(td_arr[j])



    print(len(value_arr_2), '/', value_arr_2)
    print(len(value_arr_title2), '/', value_arr_title2)
    exit()

    print('len(value_arr_title2) = ', len(value_arr_title2))
    print(value_arr_title2)
    print('len(value_arr_2)      = ', len(value_arr_2))
    print(value_arr_2)

    exit()

    if len(investment_info) < 10:
        return []

    number = 0
    for idx, val in enumerate(investment_info):
        '''
        if idx == 7 or idx == 8 or idx == 10 or idx == 11:
            continue
        else:
            var_arr = val.text.replace('\n', '').replace('\t', '').split('l')
            value_arr_2.append(var_arr[0])
            print(list_title_2[idx], '/', value_arr_2[idx])
            if len(var_arr) >= 2:
                value_arr_2.append(var_arr[1])
                print(list_title_2[idx], '/', value_arr_2[idx])
        '''
        var_arr = val.text.replace('\n', '').replace('\t', '').split('l')

        # 액면가 매매단위가 아예 없는 경우가 있다...
        # 와 이따구로할꺼면 쿼리날릴때 동적이어야 하겠는데....
        #print('var_arr[0] = ', var_arr[0])
        value_arr_2.append(var_arr[0])

        print(list_title_2[number], '/', value_arr_2[number])
        number += 1
        if len(var_arr) >= 2:
            value_arr_2.append(var_arr[1])

            print(list_title_2[number], '/', value_arr_2[number])
            number += 1

    print(len(value_arr_2))
    del value_arr_2[7]
    del value_arr_2[8-1]
    del value_arr_2[10-2]
    del value_arr_2[11-3]
    print(len(value_arr_2))
    exit()
    #print('-----------------------------')
    value_arr_1.extend(value_arr_2)
    value_arr_1.append(stock_cd)
    return value_arr_1

# SQLite DB 연결
conn = sqlite3.connect("test.db")

# Connection 으로부터 Cursor 생성
cur = conn.cursor()

cur.execute("SELECT stock_cd FROM TBL_TOTAL_INF WHERE price_day_before is null")

stock_list = cur.fetchall()

sql = """UPDATE TBL_TOTAL_INF SET
`price_day_before` = ?,
`price_hight` = ?,
`transaction_volumn` = ?,
`price_start` = ?,
`price_row` = ?,
`transaction_payment` = ?,
`market_capitalization` = ?,
`market_capitalization_rank` = ?,
`number_of_listed_shares` = ?,
`par_value` = ?,
`trad_unit` = ?,
`day_of_stockholders_meeting` = ?,
`vote` = ?,
`foreign_exhaustion_rate` = ?,
`52week_high` = ?,
`52week_row` = ?,
`per_fnguide` = ?,
`eps_fnguide` = ?,
`per_krx` = ?,
`eps_krx` = ?,
`estimated_per` = ?,
`estimated_eps` = ?,
`pbr_fnguide` = ?,
`pbs_fnguide` = ?,
`dividend_yield_ratio` = ?,
`same_industry` = ?,
`same_industry_falling_rate` = ?
WHERE stock_cd = ?"""

# 시작시간
start_time = time.time()
print('start_time = ', start_time)

_investment_info = []

stock_list_tot = len(stock_list)

number = 1

for stock in stock_list:
    # 종목 메인 request 객체 생성
    req = requests.get(get_item_main_url(stock[0]))

    # html소스를 soup = BeautifulSoup 객체로 변환
    soup = BeautifulSoup(req.text, 'html.parser')

    # 종합 정보 크롤링
    row = get_investment_info(stock[0], soup)

    if len(row) > 0:
        _investment_info.append(row)
        cur.execute(sql, row)
        conn.commit()

    print(row)
    print(number, '/', stock_list_tot)

    # 반복문 인덱스 증가
    number += 1

#cur.executemany(sql, _investment_info)

conn.commit()
# print(investment_info)
print("종료 --- seconds ---", int((time.time() - start_time)), '초')

cur.close()
conn.close()





exit()

# 039130 하나투어
# 종목 메인 request 객체 생성
_req = requests.get(get_item_main_url('039130'))

# BeautifulSoup으로 html소스를 python객체로 변환
_soup = BeautifulSoup(_req.text, 'html.parser')

# 투자정보 테스트

# 투자정보 - 시가총액
_investment_info = get_investment_info(_soup)
print(_investment_info)
