import os
import psycopg2
import json
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import time
from tickers import tickers as TICKERS


# Database connection parameters
DB_PARAMS = {
    "dbname": os.getenv("DB_NAME", "stock_data"),
    "user": os.getenv("DB_USER", "user"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "host": os.getenv("DB_HOST", "db"),
    "port": os.getenv("DB_PORT", "5432")
}

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS stock_data (
                id SERIAL PRIMARY KEY,
                symbol TEXT,
                category TEXT,
                date DATE,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                adj_close FLOAT,
                volume BIGINT,
                UNIQUE (symbol, date)
            )
        """)
    conn.commit()

def fetch_stock_data(symbol, start_date='2005-01-01'):
    end_date = datetime.now().strftime('%Y-%m-%d')
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

def get_latest_date(conn, symbol):
    with conn.cursor() as cur:
        cur.execute("SELECT MAX(date) FROM stock_data WHERE symbol = %s", (symbol,))
        result = cur.fetchone()[0]
    return result

def insert_stock_data(conn, symbol, category, data):
    with conn.cursor() as cur:
        for date, row in data.iterrows():
            cur.execute("""
                INSERT INTO stock_data (symbol, category, date, open, high, low, close, adj_close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (symbol, date) 
                DO UPDATE SET
                    category = EXCLUDED.category,
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    adj_close = EXCLUDED.adj_close,
                    volume = EXCLUDED.volume
            """, (
                symbol,
                category,
                date.date(),
                float(row['Open']),
                float(row['High']),
                float(row['Low']),
                float(row['Close']),
                float(row['Adj Close']),
                int(row['Volume'])
            ))
    conn.commit()

def save_to_local(symbol, category, data):
    filename = f"/app/data/{category}/{symbol}_data.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data.to_csv(filename)
    print(f"Data for {symbol} saved to {filename}")

def fetch_and_save_all_data(conn):
    all_data = {}
    for category, symbols in TICKERS.items():
        print(f"Preparing data for {category}")
        time.sleep(2) # api 호출 제한 피하기 위함
        all_data[category] = {}
        for symbol in symbols:
            print(f"Fetching data for {symbol} ({category})...")
            data = fetch_stock_data(symbol)
            
            if not data.empty:
                insert_stock_data(conn, symbol, category, data)
                save_to_local(symbol, category, data)
                all_data[category][symbol] = data
                print(f"Data for {symbol} processed successfully.")
            else:
                print(f"Error fetching data for {symbol}: No data returned")
    
    return all_data


def main():
    conn = psycopg2.connect(**DB_PARAMS)
    create_table(conn)

    all_data = fetch_and_save_all_data(conn)
    
    # Notify analysis service
    notify_analysis_service()
    
    conn.close()
    print("Database connection closed. All operations completed successfully!")

def notify_analysis_service():
    # This function would typically use a message queue or API call to notify the analysis service
    # For simplicity, we'll just print a message here
    print("Notifying analysis service to start processing...")
    # In a real-world scenario, you might use something like:
    # requests.post('http://analysis_service:5000/start_analysis')

if __name__ == "__main__":
    main()