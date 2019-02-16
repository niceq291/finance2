# 테이블 생성 : TBL_TOTAL_INF
'''
CREATE TABLE TBL_TOTAL_INF(
  stock_cd CHAR PRIMARY KEY NOT NULL,
  stock_nm NVARCHAR2,
  price_day_before NUMBER,
  price_start NUMBER,
  price_hight NUMBER,
  price_row NUMBER,
  transaction_volumn NUMBER,
  transaction_payment VARCHAR2,
  market_capitalization VARCHAR2,
  foreign_exhaustion_rate REAL,
  52week_high NUMBER,
  52week_row NUMBER,
  per_fnguide REAL,
  eps_fnguide NUMBER,
  per_krx REAL,
  eps_krx NUMBER,
  estimated_per REAL,
  estimated_eps NUMBER,
  pbr_fnguide REAL,
  pbs_fnguide NUMBER,
  dividend_yield_ratio REAL,
  dividend NUMBER,
  day_of_stockholders_meeting VARCHAR2,
  vote VARCHAR2)
'''