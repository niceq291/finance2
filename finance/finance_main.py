import requests
from bs4 import BeautifulSoup
import pandas as pd

# 종목 메인 url 생성
# code : 종목코드
def get_item_main_url(code):
    return 'https://finance.naver.com/item/main.nhn?code={code}'.format(code=code)

# 종목 메인 url 생성(모바일)
# code : 종목코드
def get_item_main_url_mobile(code):
    return 'https://m.stock.naver.com/item/main.nhn#/stocks/{code}/total'.format(code=code)

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

    # 039130 하나투어

    # DataFrame 생성
    df = pd.DataFrame()

    df = df.append(pd.read_html(get_item_main_url_mobile('039130'), header=0)[0], ignore_index=True)

    # 결측값 있는 행 제거
    df = df.dropna()

    # csv로 저장
    # df.to_csv('C:/Users/buttle-niceq/Desktop/a.csv', encoding='ms949')

    # 콘솔 넓이 제거
    pd.options.display.width = None
    # 콘솔 출력
    print(df)
    return ''


# 투자정보
def get_investment_info2(soup):
    investment_info = {}

    # 투자정보 시가총액
    investment_info_table = soup.select('#tab_con1 > div.first > table > tr')
    print(len(investment_info_table))


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

        #td = tr.select('td > em')
        #print(td[0].string.strip())

# 최근연간실절
# https://m.stock.naver.com/api/html/item/financialInfo.nhn?type=annual&code=039130
# 최근분기실적
# https://m.stock.naver.com/api/html/item/financialInfo.nhn?type=quarter&code=039130

    '''
    # 시가총액
    market_sum = soup.select('#_market_sum')

    investment_info['market_sum']= market_sum[0].text.strip()

    # 시가총액 단위
    market_sum_unit = soup.select('#tab_con1 > div.first > table > tr.strong > td')

    # 시가총액 (숫자+문자)
    market_sum_mix = market_sum_unit[0].text.strip()
    market_sum_mix = market_sum_mix.replace('\n', '')
    market_sum_mix = market_sum_mix.replace('\t', '')
    investment_info['market_sum_mix'] = market_sum_mix

    #print(soup)

    # 상장주식수
    stocks_count = soup.select('#tab_con1 > div.first > table > tr:nth-child(2)')
    print(stocks_count)
    print(stocks_count[0].text)

    #market_sum_unit_list = market_sum_unit_text.sp
    '''
    # 최종 확인
    print('**************************************************************')
    print(investment_info)


# 039130 하나투어
# 종목 메인 request 객체 생성
_req = requests.get(get_item_main_url('039130'))

# BeautifulSoup으로 html소스를 python객체로 변환
_soup = BeautifulSoup(_req.text, 'html.parser')

# 투자정보 테스트

# 투자정보 - 시가총액
_market_sum = get_investment_info(_soup)
#print(_market_sum)

'''
# 기업개요 테스트
summary_info_text = get_summary_info(soup)
print(summary_info_text)
'''

exit()


# 일별 시세 url 생성
# code : 종목코드
def get_sise_day_url(code):
    return 'https://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)

# 005930 삼성전자
url = get_sise_day_url('005930')
print('url:', url)

url2 = get_item_main_url('005930')
print('url2:', url2)

# DataFrame 생성
df = pd.DataFrame()

for page in range(1,40):
    pg_url = '{url}&page={page}'.format(url=url, page=page)
    print(pg_url)
    df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)
    # dfs = pd.read_html(pg_url)
    # dfs = pd.read_html('http://finance.naver.com/item/sise_day.nhn?code=005930&page=1')
    # df = dfs[0]
    # df.head()
# 결측값 있는 행 제거
df = df.dropna()

# csv로 저장
# df.to_csv('C:/Users/buttle-niceq/Desktop/a.csv', encoding='ms949')

# 콘솔 넓이 제거
pd.options.display.width = None
# 콘솔 출력
print(df)





























"""
req = requests.get('https://finance.naver.com/item/main.nhn?code=005930')

#print(req.text)

soup = BeautifulSoup(req.text, 'html.parser')

print('******************************************************')
# 고가
hightLateList = soup.select('#chart_area > div.rate_info > table > tr > td > em.no_up > span.blind')
for span in hightLateList:
    print(span.text)

print('******************************************************')
# 각 타이틀
hightLateList = soup.select('#chart_area > div.rate_info > table > tr > td > span')
for span in hightLateList:
    print(span.text)

print('******************************************************')
# 현재가
hightLateList = soup.select('div > p.no_today > em > span.blind')
for span in hightLateList:
    print(span.text)


print('******************************************************')
# rate_info
#rate_info = soup.select('div.rate_info')
rate_info = soup.select('#chart_area > div.rate_info > div.today > p > em > span.blind')
rate_info = soup.select('span.sptxt sp_txt')
print(rate_info.__len__())
for element in rate_info:
    print(element.text)
    if element.get('class') == 'today':
        print('today : ', element.text)

print('******************************************************')

# 네이버 주식 일별시세
# https://finance.naver.com/item/sise_day.nhn?code=005930&page=1
request_code = '005930'
request_url = 'https://finance.naver.com/item/sise_day.nhn?code=&page='
#req = requests.get('https://finance.naver.com/item/sise_day.nhn?code=005930&page=1')
#soup = BeautifulSoup(req.text, 'html.parser')

for page in range(1,10):
    page_url = request_url +page
    print(page_url)
"""
"""
code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]
code_df.head()

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
code_df.head()

"""