## This is a read me file that is explaining the project

![ezcv logo](https://github.com/raghav-singh-wizard/Real-Time-Financial-Data-Pipeline-and-Analytics/blob/master/Project_Architectures/project_architecture.png)


##  INDIAN STOCK MARKET

The Indian stock market serves as a crucial financial hub, reflecting the country's economic health and providing investment opportunities. It comprises two primary exchanges: the National Stock Exchange (NSE) and the Bombay Stock Exchange (BSE). Both exchanges play a pivotal role in facilitating the buying and selling of stocks, derivatives, and other financial instruments.

Investors, traders, and financial institutions engage in the stock market to buy and sell shares of publicly listed companies, aiming to generate returns based on price movements. The stock market's performance is influenced by various factors, including economic indicators, political events, corporate performance, and global market trends.

## Data retrieval from the NSE website 

Data retrieval from the NSE (National Stock Exchange) website is a pivotal facet of the data engineering project, involving the extraction of real-time financial data crucial for comprehensive analysis and decision-making in the stock market.

This process of real-time data extraction encompasses a diverse range of financial information, including stock prices, trading volumes, company financials, and market indices. The NSE website offers essential tools such as the option chain, presenting real-time options (calls and puts) available for individual stocks and indices. Notably, the option chain data is updated every 3 minutes on the NSE website (https://www.nseindia.com/option-chain), a critical aspect for the project's real-time data processing.

As a data engineering initiative, it's integral to harness this dynamically changing data for analysis. This involves understanding market trends, evaluating volatility, and measuring liquidity. Data engineers use this information to design and optimize robust data pipelines and storage systems capable of managing and processing the constant influx of financial data.

The project focuses on leveraging real-time financial data for creating efficient and scalable data structures. Data engineering strategies are employed to process, store, and deliver this data effectively. It emphasizes the development of data pipelines that can handle large volumes of rapidly updating information while ensuring reliability and accessibility.

Understanding and effectively managing this real-time data retrieval process within the realm of data engineering is vital for constructing resilient data processing systems. This project aims to design and implement systems capable of managing the dynamic flow of financial data, offering traders and investors the critical insights necessary for strategic decision-making in India's dynamic financial landscape.

## PYTHON SCRIPT FOR DATA RETRIVAL FROM NSE WEBSITE

Leveraging Python's flexibility and Pandas' robust data handling features, I crafted a proficient data retrieval script. This script systematically obtained real-time financial information from the NSE website, capturing varied data like stock prices, trading volumes, and market indices, particularly focusing on Banknifty for detailed insights.

These two function are used for the data retrival process.

### `fetch(index)`
- The `fetch` function retrieves data from the NSE website for a specified index.
- It makes a GET request to the NSE API endpoint for the option chain of the specified index.
- The retrieved data is then normalized and sorted based on expiry dates.

### `get_data(index='BANKNIFTY')`
- The `get_data` function utilizes the `fetch` function to retrieve financial data for a specified index, with 'BANKNIFTY' as the default.
- The retrieved data is then processed to filter and sort information based on expiry dates.

## CREATING TABLES AND STORING DATA IN LOCAL POSTGRESQL

In this project, I advanced my learning on  PostgreSQL database  and used using Python to store data in this local postgresql by creating tables as per use.Leveraging PostgreSQL, I executed SQL commands to define and manage tables. Through Python's psycopg2 library, I established connections to the database, executed SQL queries to create tables, and inserted retrieved financial data. This process improved my understanding of SQL, allowing efficient storage and retrieval of data for analysis, marking a significant learning curve in managing databases within the realm of data engineering and analysis.

# PostgreSQL Configuration

I used this to connect my postgresql with my python script 


```python
pg_config = {
    'host': 'localhost',
    'port': '5432',  # Change to your PostgreSQL port
    'dbName': 'stockmarket_live_data',
    'dbUser': 'myusername',
    'dbPassword': 'mypassword'
}
```

## Function to Connect to PostgreSQL Database

```python
import psycopg2

def connect_db(config):
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
```

## CREATED TABLE IN POSTGRESQL DATABASE

```commandline
def create_table(conn, table_name):
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



```

#### NOW DATA IS LOADED TO THE TABLE MADE AND NOW LOCAL POSTGRESQL CONTAINS THE REQUIRED DATA IN NON TRANSFORMED FORMAT.

#### NOW WE WILL SHIFT OUR DATA TO AZURE CLOUD BY USING ETL PIPELINE.

# AZURE CLOUD PORTAL

In the Azure Cloud Portal, I established a dedicated project environment under the resource group named "stockmarket-OI-data-PROJECT." Within this environment, I provisioned a Storage Account and created three distinct containers: "BRONZE," "SILVER," and "GOLD." Each container serves a specific data transformation stage: "BRONZE" holds raw, untransformed data, "SILVER" contains semi-transformed data, and "GOLD" stores fully transformed data.

Additionally, an Azure Synapse Analytics workspace was allocated to the same resource group, facilitating robust data analytics and warehousing capabilities. This workspace acts as the core hub for data processing and analysis. Within the resource group, an Azure Data Factory was established for efficient data orchestration, managing data movement and workflows. Furthermore, an Azure Databricks service was integrated into the resource group to enable advanced data processing and analytics, ensuring a comprehensive data engineering workflow entirely within this project's dedicated environment.

### AZURE DATA FACTORY

```
Name of ADF= 'PROJECT-STOCKMARKET-ADF'
```

![ezcv logo](https://github.com/raghav-singh-wizard/Real-Time-Financial-Data-Pipeline-and-Analytics/blob/master/Project_Architectures/ADF_PIPELINE.png)









