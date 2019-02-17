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
    if(len(summary_info_list) > 0):

        # p 태그가 여러개인 경우 내용을 합친다
        for p in summary_info_list:
            summary_info_text += p.text

    return summary_info_text


# 투자정보
def get_investment_info(soup):
    investment_info = {}

    # 투자정보 시가총액
    investment_info_tbl = soup.select('#tab_con1 > div.first > table > tr')

    for idx, val in enumerate(investment_info_tbl):
        th = val.select('th')[0]
        td = val.select('td')[0]

        if idx == 3:
            title = th.text.split('l')
            value = td.text.replace('\t', '').replace('\n', '').replace(',', '').split('l')

        elif idx == 4:
            title = th.text.split('l')
            value = td.text.replace('\t', '').replace('\n', '').replace(',', '').split('l')
        else:
            title = th.text.replace('\t', '').replace('\n', '')
            value = td.text.replace('\t', '').replace('\n', '').replace(',', '')


        print(title, '\t\t', value)
        print('-----------------------------')



    # print(investment_info)
    exit()
    # 외국인 소진율
    # #tab_con1 > div:nth-child(3) > table

    # 투자의견, 목표주가 ,52주 최고/최저
    # #tab_con1 > div:nth-child(4) > table

    # PER
    # #tab_con1 > div:nth-child(5) > table

    # 동일업종 PER
    # #tab_con1 > div:nth-child(6) > table


    for tr in investment_info_table:
        print('----------------------------------------------------------------')
        # <class 'bs4.element.Tag'>
        #print(type(tr))
        th = tr.select('th')
        th_text = ''

        if th[0].string is None:
            print('if th[0].string is None')
            a = tr.select('th > a')
            #print(type(a))
            #print(a)
            if len(a) > 0:
                #print(a[0].string)
                th_text = a[0].text
            else:
                print(a)
        else:
            th_text = th[0].text

        print('TH = ', th_text)
        print('>')

    # 최종 확인
    print('**************************************************************')
    print(investment_info)

    return investment_info

# 039130 하나투어
# 종목 메인 request 객체 생성
_req = requests.get(get_item_main_url('039130'))

# BeautifulSoup으로 html소스를 python객체로 변환
_soup = BeautifulSoup(_req.text, 'html.parser')

# 투자정보 테스트

# 투자정보 - 시가총액
_investment_info = get_investment_info(_soup)
print(_investment_info)
