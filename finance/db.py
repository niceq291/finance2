import sqlite3

# SQLite DB 연결
conn = sqlite3.connect("test.db")

# Connection 으로부터 Cursor 생성
cur = conn.cursor()

# 테이블 확인
cur.execute("SELECT * FROM sqlite_master WHERE type = 'table' AND name = 'TBL_TOTAL_INF'")

# 테이블 조회 결과
rows = cur.fetchall()

# 테이블이 존재 하지 않을경우 테이블 생성
if len(rows) < 1:
    CREATE_TBL_TOTAL_INF = 'CREATE TABLE [TBL_TOTAL_INF]([stock_cd] CHAR PRIMARY KEY NOT NULL, [stock_nm] NVARCHAR2, [price_day_before] NUMBER, [price_start] NUMBER, [price_hight] NUMBER, [price_row] NUMBER, [transaction_volumn] NUMBER, [transaction_payment] VARCHAR2, [market_capitalization] VARCHAR2, [foreign_exhaustion_rate] REAL, [52week_high] NUMBER, [52week_row] NUMBER, [per_fnguide] REAL, [eps_fnguide] NUMBER, [per_krx] REAL, [eps_krx] NUMBER, [estimated_per] REAL, [estimated_eps] NUMBER, [pbr_fnguide] REAL, [pbs_fnguide] NUMBER, [dividend_yield_ratio] REAL, [dividend] NUMBER, [day_of_stockholders_meeting] VARCHAR2, [vote] VARCHAR2)'
    cur.execute(CREATE_TBL_TOTAL_INF)


sql = "insert into TBL_TOTAL_INF(stock_cd,stock_nm) values (?, ?)"
data = (
    ('하나투어', '039130'),
    ('삼성전자', '005930'),
    ('카카오', '035720')
)
cur.executemany(sql, data)
conn.commit()



conn.close()
exit()


# SQL 쿼리 실행
cur.execute("select * from customer")

# 데이타 Fetch
rows = cur.fetchall()
for row in rows:
    print(row)

# Connection 닫기
conn.close()