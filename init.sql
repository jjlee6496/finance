\c stock;

-- 테이블이 존재하지 않는 경우에만 생성합니다.
CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY,
    category TEXT,
    symbol TEXT,
    date DATE,
    open FLOAT,
    high FLOAT,
    low FLOAT,
    close FLOAT,
    adj_close FLOAT,
    volume BIGINT,
    UNIQUE (symbol, date)
);