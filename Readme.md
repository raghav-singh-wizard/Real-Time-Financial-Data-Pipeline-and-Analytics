## This is a read me file that is explaining the project

![ezcv logo](https://github.com/raghav-singh-wizard/Real-Time-Financial-Data-Pipeline-and-Analytics/blob/master/Project_Architectures/project_architecturee.png)

#### Project Title - Real-Time-Financial-Data-Pipeline-and-Analytics 
### OVERVIEW
This project revolves around leveraging data engineering techniques and analytical methodologies to comprehend the Indian stock market dynamics.The primary objective is to capture real-time data from the NSE website and subsequently transferring it to local PostgreSQL and then to the Azure Synapse Analytics warehouse is a key goal of the project. The  harnessed data will enable comprehensive analysis of stock market trends and key financial indicators. This includes leveraging data engineering techniques and analytical methodologies to process, store, and subsequently analyze the collected data.

### Goals:

1. **Data Retrieval from NSE:** Acquire real-time financial data encompassing stock prices, options, and market indices, focusing on streamlining its processing.
2. **Data Management:** Implement efficient data storage structures, ensuring systematic data transformation and cleansing.
3. **Cloud Migration:** Transfer data from local PostgreSQL to Azure Cloud for real-time updates in the cloud environment.
4. **Azure Data Orchestration:** Develop Azure Data Factory pipelines designed for orchestrated data movement and transformation.
5. **Azure Synapse Integration:** Integrate Azure Synapse Analytics for streamlining big data analytics and providing actionable insights.
6. **Pipeline Automation:** Utilize Azure Data Factory pipelines to trigger regular data retrieval from the NSE site every 5 minutes for automated data collection.

### Challenges:

1. **Real-time Data Extraction:** Capturing live financial data updates every 3 minutes from the NSE site.
2. **Data Transformation and Structure:** Converting raw financial data into a structured, analyzable format.
3. **Cloud Data Migration:** Facilitating the seamless transition of data from the local PostgreSQL database to the Azure cloud environment.
4. **Automation and Pipeline Triggers:** Implementing periodic pipeline executions in alignment with NSE data refresh cycles for continuous data collection.

### Project Flow:

1. **Data Retrieval and Local Storage:** A Python script retrieves financial data from the NSE site and stores it in a local PostgreSQL database.
2. **Cloud Migration and Orchestration:** Data is migrated from local PostgreSQL to Azure Data Lake Gen2 containers, progressing through Bronze, Silver, and Gold stages for various transformations.
3. **Azure Data Orchestration:** Azure Data Factory orchestrates the movement and processing of data, ensuring efficient workflows.
4. **Data Transformation:** Azure Databricks refines and transforms data from Silver to Gold stages, enhancing its quality and structure.
5. **Pipeline Automation:** Azure Data Factory pipelines are configured to execute every 6 minutes, enabling real-time data retrieval from the NSE site and further processing within Azure Synapse Analytics.


### INDIAN STOCK MARKET

The Indian stock market serves as a crucial financial hub, reflecting the country's economic health and providing investment opportunities. It comprises two primary exchanges: the National Stock Exchange (NSE) and the Bombay Stock Exchange (BSE). Both exchanges play a pivotal role in facilitating the buying and selling of stocks, derivatives, and other financial instruments.

Investors, traders, and financial institutions engage in the stock market to buy and sell shares of publicly listed companies, aiming to generate returns based on price movements. The stock market's performance is influenced by various factors, including economic indicators, political events, corporate performance, and global market trends.

## Data retrieval from the NSE website 

Data retrieval from the NSE (National Stock Exchange) website is a pivotal facet of the data engineering project, involving the extraction of real-time financial data crucial for comprehensive analysis and decision-making in the stock market.

This process of real-time data extraction encompasses a diverse range of financial information, including stock prices, trading volumes, company financials, and market indices. The NSE website offers essential tools such as the option chain, presenting real-time options (calls and puts) available for individual stocks and indices. Notably, the option chain data is updated every 3 minutes on the NSE website (https://www.nseindia.com/option-chain), a critical aspect for the project's real-time data processing.

As a data engineering initiative, it's integral to harness this dynamically changing data for analysis. This involves understanding market trends, evaluating volatility, and measuring liquidity. Data engineers use this information to design and optimize robust data pipelines and storage systems capable of managing and processing the constant influx of financial data.

The project focuses on leveraging real-time financial data for creating efficient and scalable data structures. Data engineering strategies are employed to process, store, and deliver this data effectively. It emphasizes the development of data pipelines that can handle large volumes of rapidly updating information while ensuring reliability and accessibility.

Understanding and effectively managing this real-time data retrieval process within the realm of data engineering is vital for constructing resilient data processing systems. This project aims to design and implement systems capable of managing the dynamic flow of financial data, offering traders and investors the critical insights necessary for strategic decision-making in India's dynamic financial landscape.

## PYTHON SCRIPT FOR DATA RETRIVAL FROM NSE WEBSITE [](https://github.com/raghav-singh-wizard/Real-Time-Financial-Data-Pipeline-and-Analytics/blob/master/rks_new_oi.py)

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
### PIPELINE DIAGRAM 
![ezcv logo](https://github.com/raghav-singh-wizard/Real-Time-Financial-Data-Pipeline-and-Analytics/blob/master/Project_Architectures/ADF_PIPELINE.png)

### LOOKUP ACTIVITY 

The Lookup activity in Azure Data Factory retrieves metadata or control information from diverse sources like Azure Blob Storage, Azure SQL Database, or other databases. This component, integral to data pipelines, allows querying without altering data. It's pivotal for acquiring filenames, table names, or configuration details required for subsequent data processing. With support for SQL or custom queries and parameterization, it seamlessly integrates within the pipeline, ensuring adaptability and flexibility. Used widely in pre-processing scenarios, the Lookup activity serves as a bridge, facilitating the retrieval of necessary information to drive subsequent data transformations within Azure Data Factory

```It requires a source dataset .```

I utilized Azure's Runtime Integration Software to configure my personal computer as a node, facilitating the seamless connection between an on-premises PostgreSQL database and the cloud infrastructure. This integration process establishes a secure and efficient link, enabling data interaction and transfer between the local PostgreSQL system and the Azure cloud environment. By configuring my PC as a node, I ensured a smooth, reliable connection, empowering the exchange of data and operations between the on-premises database and Azure cloud resources. This setup optimizes accessibility and data flow, enhancing the interoperability and functionality of the entire system.

I employed the Lookup activity's query option to retrieve a list of all tables in my database using the SQL query:

```commandline
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
```
With this information, I leveraged the FOR EACH activity, using dynamic content in the pipeline expression builder:

```commandline
@activity('alltableindatabase').output.value
```

Next, I executed a Copy Data activity within the FOR EACH activity. To source my data, I established a linked service for my local PostgreSQL database, enabling a connection between my local and cloud environments. I employed dynamic querying:

```commandline
@if(equals(item().table_name, 'marketdata'), 
'select * from marketdata ORDER BY curr_time DESC 
LIMIT 27;', concat('select * from ', item().table_name))
```

Data was then deposited into an Azure Data Lake Gen2 Bronze container. At this stage, the data remained untransformed, residing in the Azure cloud, ready for further processing and analysis.

## AZURE DATABRICKS

Utilizing Databricks, I performed data transformation, refining and enriching the retrieved information. Azure Data Factory (ADF) orchestrated the process, directing the transformed data into Azure Data Lake Gen2 (ADLGen2). The integrated workflow ensured seamless data movement and storage, facilitating the refined dataset's secure storage within the Data Lake. This collaborative effort between Databricks, ADF, and ADLGen2 enabled efficient transformation and subsequent storage of the processed data, laying a robust foundation for further analytical endeavors and ensuring easy access to the enriched dataset.

##### NOTEBOOK 1: Bronze to Silver Transformation
##### NOTEBOOK 2: Silver to Gold for Stock Market Project```

```***************************************************```
### Notebook 1 information with clear and concise documentation:

```python

# Connecting Azure Data Lake with Azure Databricks Using Container Access Keys

spark.conf.set(
    "fs.azure.account.key.projectstockmarket.dfs.core.windows.net",
    "YOUR CONTAINER ACCESS KEY"
)

# Defining Input Path
input_path = "abfss://bronze@projectstockmarket.dfs.core.windows.net/dile"

# Reading and Transforming Data
df = spark.read.format("csv") \
    .option("inferSchema", "true") \
    .option("header", "true") \
    .option("delimiter", ",") \
    .load(input_path)

# NOTEBOOK 1: Bronze to Silver Transformation
from pyspark.sql.functions import col
numeric_columns = ['strike', 'pe_open_intrst', 'ce_open_intrst', 'cechoi', 'cepchoi', 'pechoi', 'pepchoi',
                   'ce_total_trade_vol', 'pe_total_trade_vol', 'ce_buy_qty', 'ce_sell_qty', 'pe_buy_qty', 'pe_sell_qty', 'price']

for column in numeric_columns:
    df = df.withColumn(column, col(column).cast("double"))

from pyspark.sql.functions import to_date
from pyspark.sql.types import DateType

# Convert "expirydate" to a date
df = df.withColumn("expirydate", to_date(df["expirydate"]).cast(DateType()))

# Convert "curr_date" to a date
df = df.withColumn("curr_date", to_date(df["curr_date"]).cast(DateType()))

# Output Path for Storing the Transformed Data
output_path = "abfss://silver@projectstockmarket.dfs.core.windows.net/silver_delta_lake"

# Writing the Transformed Data to Delta Lake in the Silver Container
df.write.format("delta").mode("overwrite").save(output_path)
```

This optimized version condenses the process and ensures clarity in each step from accessing the data to transforming it and saving it into the designated storage location in the Delta Lake format within the Silver container of Azure Data Lake. 

### Notebook 2 information with clear and concise documentation:

```python
# Setting Azure Data Lake connection and Input Path
spark.conf.set(
    "fs.azure.account.key.projectstockmarket.dfs.core.windows.net",
    "YOUR CONTAINER ACCESS KEY"
)

gold_input_path = "abfss://silver@projectstockmarket.dfs.core.windows.net"

# Reading semi Transformed Data from Silver Layer
df = spark.read.format("delta").load(gold_input_path)

# NOTEBOOK 2: Silver to Gold Transformation

# Data Formatting: Changing Date and Time Formats
from pyspark.sql.functions import date_format

date_format_pattern_date = "dd/MM/yyyy"
date_format_pattern_date_time = "dd/MM/yyyy HH:mm:ss"

df = df.withColumn("expirydate", date_format(df["expirydate"], date_format_pattern_date))
df = df.withColumn("curr_date", date_format(df["curr_date"], date_format_pattern_date))

df = df.withColumn("curr_time", date_format(df["curr_time"], date_format_pattern_date_time))

# Defining Output Path for Gold Container
gold_output_path = "abfss://gold@projectstockmarket.dfs.core.windows.net"

# Writing Fully Transformed and Cleaned Data to Gold Delta Lake
df.write.format("delta").mode("overwrite").save(gold_output_path)

```
 This code efficiently performs the necessary steps, including the Azure Data Lake connection, data reading, formatting, and the final storage of fully transformed and cleaned data in the Gold container using Delta Lake format. 


The data orchestration, loading, and transformation stages are finished. The cleaned and transformed dataset now resides in the Gold Delta Lake container. This refined dataset is well-structured and prepared, facilitating advanced analytics, insightful exploration, and strategic decision-making for the project's next phases. 


Additionally, our pipeline is fully operational, enabling seamless data transfer from local PostgreSQL to Azure Gold Delta Lake whenever the pipeline is executed. This seamless data flow streamlines the process and ensures the continuous enrichment of the Gold Delta Lake with fresh, local PostgreSQL data upon pipeline activation.

### PIPELINE TRIGGER
To maintain real-time data integration from the NSE site, I've configured the data retrieval in Python to refresh every 5 minutes, aligning with the site's 3-minute data updates. To ensure continuous and timely data ingestion, I've established an Azure Data Factory pipeline triggered to execute every 6 minutes. This setup guarantees that the pipeline operates at the same frequency as the data refresh on the NSE site, enabling a consistent and up-to-date stream of information for our project's data analysis and processing needs.

## AZURE SYNAPSE ANALYTICS

Azure Synapse Analytics is a comprehensive cloud-based analytics service offering powerful capabilities for data integration, warehousing, and big data analytics. It seamlessly unifies big data and data warehousing to streamline data processing and analysis. With its integration of Apache Spark and SQL, it enables me to process and analyze large volumes of data for actionable insights. Synapse Analytics supports various data types and offers scalable resources, facilitating efficient data exploration, machine learning, and business intelligence. Its unified platform empowers me to derive valuable insights, make data-driven decisions, and optimize my business strategies, serving as a crucial component for comprehensive data management and analytics in my project.

NOW Azure Synapse Analytics features an automatic linked service to Azure Data Lake Gen2, enabling direct data retrieval. For our project, the objective is to house our data within the Azure Synapse Analytics warehouse. To achieve this, I established a linked service to a SQL database supported by Azure Synapse Analytics. Utilizing a serverless endpoint, ```stockmarketdbsynapse-ondemand.sql.azuresynapse.net```, I efficiently loaded the data from Azure Gold Delta Lake to this SQL database within Azure Synapse Analytics using a linked serverless endpoint. This streamlined process facilitates the transfer and consolidation of our data for comprehensive analytics within the Synapse environment.

#### The project is successfully concluded with our local PostgreSQL data seamlessly stored in the Azure Synapse Analytics warehouse every 5 minutes upon pipeline execution. This real-time data transfer marks the completion of our primary objective. The consolidated data will now serve as the cornerstone for generating insights and conducting diverse analyses. It enables a wide array of applications and opens avenues for in-depth exploration, empowering us to derive valuable insights and make informed decisions using this data present in our warehouse.

# Conclusion:

The Real-Time Financial Data Pipeline and Analytics project culminates in a seamless NSE-to-Azure cloud pipeline. Leveraging Python, Pandas, SQL, Azure services like Data Factory, Databricks, PostgreSQL, and Synapse Analytics, it orchestrates a robust ETL framework for NSE's option chain data. This structured dataset fuels strategic decision-making and yields valuable insights for market participants.
