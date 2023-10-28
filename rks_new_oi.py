import os
import psycopg2
import pandas as pd
import requests
import json
from datetime import datetime
import time

# Your configuration for PostgresSQL


pg_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'dbName': os.getenv('DB_NAME', 'stockmarket_live_data'),
    'dbUser': os.getenv('DB_USER'),
    'dbPassword': os.getenv('DB_PASSWORD')
    }

table_name = 'marketdata'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
    "Referer": "https://www.nseindia.com",
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Sec-Fetch-User': '?1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
}


def fetch(index: str) -> str:
    """

    :param index: nse index name
    :return: return the data fetched from the webside
    """
    r_bytes = requests.get('https://www.nseindia.com/api/option-chain-indices?symbol=' + index, headers=headers,
                           verify=True, timeout=(5, 14)).content
    my_json = r_bytes.decode('utf8').replace("'", '"')
    return my_json


def get_data(index: str = 'BANKNIFTY') -> pd.DataFrame:
    """

    :param index: index of market
    :return: structured data in pandas dataframe
    """
    data = fetch(index)
    dfdata = pd.json_normalize(json.loads(data)["records"]["data"])
    dfdata = dfdata.sort_values('expiryDate', ascending=False)
    filter_dates = sorted(dfdata['expiryDate'].unique(), reverse=False)
    dfdata = dfdata[dfdata['expiryDate'].isin(filter_dates[:3])]
    sorted_df = dfdata.sort_values(by='expiryDate', ascending=True)
    return sorted_df


def process_data(data: pd.DataFrame) -> pd.DataFrame:
    """

    :param data: Structured pandas dataframe from the market
    :return: filters rows based on 4 strike price  above and below the running strike price
    """
    df = data[['strikePrice', 'expiryDate',
               'PE.openInterest', 'CE.openInterest',
               'CE.changeinOpenInterest', 'CE.pchangeinOpenInterest',
               'PE.changeinOpenInterest', 'PE.pchangeinOpenInterest',
               'CE.totalTradedVolume', 'PE.totalTradedVolume',
               'CE.totalBuyQuantity', 'CE.totalSellQuantity',
               'PE.totalBuyQuantity', 'PE.totalSellQuantity',
               'CE.underlyingValue'
               ]]
    df.fillna(0, inplace=True)

    strprice = df["CE.underlyingValue"].values

    if len(strprice) > 0:
        strprice = max(strprice)
    else:
        k = df["CE.underlyingValue"].unique()
        try:
            strprice = max(list(set(list(k))))
        except:
            strprice = 44000

    nearest_strike = round(strprice / 100) * 100
    df = df[(df["strikePrice"] >= int(nearest_strike) - 400) & (
            df["strikePrice"] <= int(nearest_strike) + 400)]

    return df


def rename_columns(df):
    """

    :param df: pandas dataframe
    :return: rename the columns
    """
    df = df.rename(columns={'PE.openInterest': "PE_Open_intrst",
                            'CE.openInterest': "CE_Open_intrst",
                            'CE.changeinOpenInterest': 'CEchOI',
                            'PE.changeinOpenInterest': 'PEchOI',
                            'PE.pchangeinOpenInterest': 'PEpchoi',
                            'CE.pchangeinOpenInterest': 'CEpchoi',
                            'CE.totalTradedVolume': 'CE_total_trade_Vol',
                            'PE.totalTradedVolume': 'PE_total_trade_Vol',
                            'PE.totalBuyQuantity': 'PE_Buy_Qty',
                            'PE.totalSellQuantity': 'PE_Sell_Qty',
                            'CE.totalBuyQuantity': 'CE_Buy_Qty',
                            'CE.totalSellQuantity': 'CE_Sell_Qty',
                            'CE.underlyingValue': 'price',
                            'strikePrice': 'strike'})

    df = df.sort_values(by='expiryDate', ascending=True)
    return df


def connect_db(config: dict) -> [None,any]:
    """

    :param config: configuration to connect with Database
    :return: db connection if success else None
    """
    print("Connecting to PostgreSQL Database")
    conn = None
    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['dbName'],
            user=config['dbUser'],
            password=config['dbPassword']
        )
        print("Connected to PostgreSQL Database")
    except Exception as e:
        print("Error connecting to PostgreSQL")
        print(e)
    return conn


def create_table(conn, table_name):
    """

    :param conn: database connection
    :param table_name: Name of Table
    :return: None
    """
    try:
        with conn.cursor() as conn_cursor:
            conn_cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
            create_table_query = f'''
                CREATE TABLE {table_name} (
                    strike INT,
                    expiryDate DATE,
                    PE_Open_intrst FLOAT,
                    CE_Open_intrst FLOAT,
                    CEchOI FLOAT,
                    CEpchOI FLOAT,
                    PEchOI FLOAT,
                    PEpchOI FLOAT,
                    CE_total_trade_Vol FLOAT,
                    PE_total_trade_Vol FLOAT,
                    CE_Buy_Qty FLOAT,
                    CE_Sell_Qty FLOAT,
                    PE_Buy_Qty FLOAT,
                    PE_Sell_Qty FLOAT,
                    price FLOAT,
                    curr_date DATE,
                    curr_time TIME
                );
            '''
            conn_cursor.execute(create_table_query)
        conn.commit()
        print(f"Successfully created table {table_name}")
    except Exception as e:
        print("Error creating table")
        print(e)


def close_connection(conn):
    """

    :param conn: db connection
    :return: closes connection
    """
    conn.close()


def insert_into_db(conn, table_name, data):
    """

    :param conn: db connection
    :param table_name: Name of table
    :param data: Insert pandas dataframe rows into database
    :return:
    """
    values = data.to_records(index=False).tolist()
    insert_query = f"INSERT INTO {table_name} (strike, expiryDate, PE_Open_intrst, CE_Open_intrst, \
                    CEchOI, CEpchOI, PEchOI, PEpchOI, CE_total_trade_Vol, PE_total_trade_Vol, CE_Buy_Qty, CE_Sell_Qty, \
                    PE_Buy_Qty, PE_Sell_Qty, price, curr_date, curr_time) VALUES \
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        with conn.cursor() as cur:
            cur.executemany(insert_query, values)
        conn.commit()
        print("Successfully inserted data into PostgreSQL Database")
    except Exception as e:
        print("Error inserting data into PostgreSQL")
        print(e)


def main():
    conn = connect_db(pg_config)
    if conn:
        create_table(conn, table_name)
        while True:
            try:
                df = get_data()
                df = process_data(df)
                df = rename_columns(df)
                df['curr_date'] = datetime.now().date()
                df['curr_time'] = datetime.now().strftime('%H:%M:%S')
                insert_into_db(conn, table_name, df)
                time.sleep(300)  # Sleep for 5 minutes
            except Exception as e:
                print(e)
                time.sleep(300)  # Sleep for 5 minutes before retrying


if __name__ == "__main__":
    main()
