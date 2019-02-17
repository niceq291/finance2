import sqlite3
import pandas as pd


# csv 파일을 해석하여 dataframe으로 변환하고, stock_data 변수에 저장
# 종목코드 자료형 지정(지정안할 경우 숫자형으로 인식하여 앞의 0이 삭제된다)
stock_data = pd.read_csv('data.csv', dtype={'종목코드':'str'})
print(' csv 파일을 해석하여 dataframe으로 변환하고, stock_data 변수에 저장')

# 종목코드 컬럼만 선택하여 stock_code 변수에 저장
stock_code = stock_data[['종목코드', '기업명']]

# SQLite DB 연결
conn = sqlite3.connect("test.db")

# SQLite DB Connection 사용후 닫기
with conn:

    # Connection 으로부터 Cursor 생성
    cur = conn.cursor()

    # 테이블 확인
    cur.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'TBL_TOTAL_INF'")

    # 테이블 조회 결과
    rows = cur.fetchall()

    # 테이블이 존재 하지 않을경우 테이블 생성
    if len(rows) < 1:
        CREATE_TBL_TOTAL_INF = """CREATE TABLE [TBL_TOTAL_INF]
        ([stock_cd] TEXT PRIMARY KEY NOT NULL, 
        [stock_nm] NVARCHAR2, 
        [price_day_before] NUMBER, 
        [price_start] NUMBER, 
        [price_hight] NUMBER, 
        [price_row] NUMBER, 
        [transaction_volumn] NUMBER, 
        [transaction_payment] VARCHAR2, 
        [market_capitalization] VARCHAR2, 
        [foreign_exhaustion_rate] REAL, 
        [52week_high] NUMBER, 
        [52week_row] NUMBER, 
        [per_fnguide] REAL, 
        [eps_fnguide] NUMBER, 
        [per_krx] REAL, 
        [eps_krx] NUMBER, 
        [estimated_per] REAL, 
        [estimated_eps] NUMBER, 
        [pbr_fnguide] REAL, 
        [pbs_fnguide] NUMBER, 
        [dividend_yield_ratio] REAL, 
        [dividend] NUMBER, 
        [day_of_stockholders_meeting] VARCHAR2, 
        [vote] VARCHAR2)"""

        cur.execute(CREATE_TBL_TOTAL_INF)

    # INSERT
    cur.executemany('INSERT OR REPLACE INTO TBL_TOTAL_INF(stock_cd,stock_nm) values (?, ?)', stock_code.values)

    # Commit
    conn.commit()