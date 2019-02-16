import sqlite3
import pandas as pd


# csv 파일을 해석하여 dataframe으로 변환하고, stock_data 변수에 저장
stock_data = pd.read_csv('data.csv')
print(' csv 파일을 해석하여 dataframe으로 변환하고, stock_data 변수에 저장')

# 종목코드 컬럼만 선택하여 stock_code 변수에 저장
stock_code = stock_data[['종목코드', '기업명']]

# SQLite DB 연결
conn = sqlite3.connect("test.db")

# Connection 으로부터 Cursor 생성
cur = conn.cursor()

# INSERT
cur.executemany('INSERT OR REPLACE INTO TBL_TOTAL_INF(stock_cd,stock_nm) values (?, ?)', stock_code.values)

# Commit
conn.commit()

# SQLite DB 연결 해제
conn.close()