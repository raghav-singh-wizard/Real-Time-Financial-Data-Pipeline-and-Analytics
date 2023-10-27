import streamlit as st
import pandas as pd
import plotly.express as px
import time


import pandas as pd
import requests
import json
from datetime import datetime
from datetime import datetime ,time as dtime
import os



headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
            "Referer": "https://www.nseindia.com",
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Sec-Fetch-User': '?1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',}

def fetch(index):
    r_bytes = requests.get('https://www.nseindia.com/api/option-chain-indices?symbol='+index,headers=headers, 
                           verify=True,timeout=(5, 14)).content
    my_json = r_bytes.decode('utf8').replace("'", '"')
    #r = json.dumps(json.loads(my_json), indent=4, sort_keys=True)
    return my_json

def get_data(index = 'BANKNIFTY') :
    data = fetch(index)
    dfdata = pd.json_normalize(json.loads(data)["records"]["data"])
    dfdata = dfdata.sort_values('expiryDate',ascending=False)
    filter_dates = sorted(dfdata['expiryDate'].unique(), reverse=False)
    dfdata = dfdata[dfdata['expiryDate'].isin(filter_dates[:3])]
    sorted_df = dfdata.sort_values(by='expiryDate', ascending=True)
    return sorted_df



def process_data(data):
    df = data[['strikePrice' ,  'expiryDate',
            'PE.openInterest','CE.openInterest',
            'CE.changeinOpenInterest','CE.pchangeinOpenInterest',
             'PE.changeinOpenInterest','PE.pchangeinOpenInterest',
             'CE.totalTradedVolume', 'PE.totalTradedVolume',
             'CE.totalBuyQuantity','CE.totalSellQuantity',
              'PE.totalBuyQuantity','PE.totalSellQuantity',
            'CE.underlyingValue'
             ]]
    df.fillna(0,inplace=True)
    strprice = df["CE.underlyingValue"].values
    
    if len(strprice)>0:
        strprice = max(strprice)
    else:
        k = df["CE.underlyingValue"].unique() 
        try:
            strprice = max(list(set(list(k))))
        except:
            strprice = 44000
    print(strprice)
    nearest_strike = round(strprice / 100) * 100
    df = df[(df["strikePrice"] >= int(nearest_strike) - 400) & (
                    df["strikePrice"] <= int(nearest_strike) + 400)]

    return df
        

def rename_columns(df):
    df = df.rename(columns = {'PE.openInterest' : "PEOI",
                          'CE.openInterest' : "CEOI",
                          'CE.changeinOpenInterest' : 'CEchOI',
                          'PE.changeinOpenInterest': 'PEchOI',
                          'PE.pchangeinOpenInterest':'PEpchoi',
                          'CE.pchangeinOpenInterest': 'CEpchoi',
                          'CE.totalTradedVolume': 'CEVol',
                          'PE.totalTradedVolume' : 'PEVol',
                           'PE.totalBuyQuantity' : 'PEBuyQty',
                            'PE.totalSellQuantity': 'PESellQty',
                            'CE.totalBuyQuantity' : 'CEBuyQty',
                            'CE.totalSellQuantity': 'CESellQty',
                          'CE.underlyingValue' : 'price',
                          'strikePrice': 'strike' })

    df =  df.sort_values(by='expiryDate', ascending=True)
    return df


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created successfully.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def market_analysis():
    path = "data"
    df = get_data()
    df = process_data(df)
    df = rename_columns(df)
    df['current_date'] = datetime.now().date()
    df['current_time'] = datetime.now().strftime('%H:%M:%S')
    date =  "date"+str(datetime.now().date()).replace("-","_")
    filename = "oi_data.csv"
    try : 
        df_all = pd.read_csv(os.path.join(path,date,filename))
    except:
        
        create_folder_if_not_exists(os.path.join(path,date))
        df_all = pd.DataFrame()
    df_all = pd.concat([df_all,df],ignore_index=True)
    df_all.to_csv(os.path.join(path,date,filename),index=None)
    return df_all
    



# Create a Streamlit app
st.title("Summary Statistics")

# Define a function to generate and update the bar charts
def update_bar_charts(summary_data):
    # Separate the mean and standard deviation values
    mean_values = summary_data.loc['mean']
    std_values = summary_data.loc['std']

    # Create bar charts using Plotly Express
    fig_mean = px.bar(mean_values[['PEOI', 'CEOI']], barmode='group')
    fig_mean.update_layout(title='Mean of PEOI vs CEOI', xaxis_title='Category', yaxis_title='Mean')

    fig_mean_buy = px.bar(mean_values[['PEBuyQty', 'CEBuyQty']], barmode='group')
    fig_mean_buy.update_layout(title='Mean of pe vs CE buy', xaxis_title='Category', yaxis_title='Mean')

    fig_std = px.bar(mean_values[['CESellQty', 'PESellQty']], barmode='group')
    fig_std.update_layout(title='Smean of sell ce vs pe', xaxis_title='Category', yaxis_title='Mean ')

    # Display the charts using Streamlit
    st.plotly_chart(fig_mean, use_container_width=True)
    st.plotly_chart(fig_mean_buy, use_container_width=True)
    st.plotly_chart(fig_std, use_container_width=True)

def transform(df_curr,df_prev):
    merged_df = pd.merge(df_curr, df_prev, on=['strike','current_date','expiryDate'], suffixes=('_df1', '_df2'))
    # Subtract the values from df2 columns from the values in df1 columns
    subtract_columns = [col  for col in df_prev.columns if col not in ['strike','current_date','expiryDate']]
    res_df = pd.DataFrame()
    res_df['strike'] = merged_df['strike']
    res_df['expiryDate'] = merged_df['expiryDate']
    res_df['current_date'] = merged_df['current_date']
    for col in subtract_columns:
        res_df[col] = merged_df[col + '_df1'] - merged_df[col + '_df2']

    return res_df

def data_mainpulation(df:pd.DataFrame):
    list_df = []
    exp_date = sorted(df['expiryDate'].unique())
    df = df[df['expiryDate'] == exp_date[0]]
    df = df.sort_values(by='current_time',ascending=True).reset_index(drop=True)
    df2 = df.copy()
    unique = df2['current_time'].unique()
    for t in range(1,len(unique)):
        df_prev = df2[df2['current_time']== unique[t-1]].drop('current_time',axis=1).sort_values('strike').reset_index(drop=True)
        df_curr = df2[df2['current_time']== unique[t]].drop('current_time',axis=1).sort_values('strike').reset_index(drop=True)
        res_df = transform(df_curr,df_prev)
        res_df['current_time'] = unique[t]
        list_df.append([res_df,unique[t]])
    if list_df:
        return list_df
    else:
        return [df,df['current_time'].unique()[0]]

placeholder1 ,placeholder2 = st.empty() , st.empty()
# Continuously update the bar charts every second
while True:
    # Update the summary data here with your dynamic data source
    start_time = dtime(9, 15)
    end_time = dtime(15, 30) 
    current_datetime = datetime.now()
    current_time = current_datetime.time()
    if current_datetime.weekday() < 5 and (start_time < current_time < end_time):  
        df = market_analysis()
        list_data = data_mainpulation(df)
        with placeholder1.container():
            c = 0
            if len(list_data)>0:
                print(list_data)
                times = [t[1] for t in list_data]
                tabs = placeholder1.tabs([f'{t} time ' for t in times])
                for tab in tabs:
                    with tab:
                        st.header(f"{times[c][1]} market Time")
                        data = list_data[c][0]
                        st.table(data.round(2).style.highlight_max(axis=0))
                        c+=1
        
        with placeholder2.container():
            summary_data = df.describe()
            st.subheader("Summary Data")
            update_bar_charts(summary_data)

        # Wait for 1 second before updating again
        time.sleep(300)

    else:
        time.sleep(300)