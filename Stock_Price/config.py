import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()
my_email = os.getenv("MY_EMAIL")
password = os.getenv("EMAIL_PASSWORD")
stock_news_api: str= "7b5eb22fa9ff49018c6441345c84fc47"
stock_news_endpoint: str= "https://newsapi.org/v2/everything"
news_name: str="TSLA"
azi_date = datetime.now()
azi_str: str= azi_date.strftime('%Y-%m-%d')
acum_3_zile_date = azi_date - timedelta(days=3)
acum_3_zile_str = acum_3_zile_date.strftime('%Y-%m-%d')

# 2. Setăm parametrii corecți conform documentației /everything
param_stock_news = {
    "apiKey": stock_news_api,
    "qInTitle": news_name,
    "q": "stock OR shares OR earnings OR market OR dividend",
"domains": "finance.yahoo.com, marketwatch.com, reuters.com, bloomberg.com, cnbc.com, wsj.com, fool.com",

    "language": "en",
    "from": acum_3_zile_str,
    "to": azi_str,
    "sortBy": "relevancy"
}
stock_price_api:str="LXSEELAGPIJ9QDZ6"
stock_end_point : str="https://www.alphavantage.co/query"
time_series: str="TIME_SERIES_DAILY"
symbol:str="AAPL"
interval:str="1min"
param_stock_price={
    "function":time_series,
    "symbol":symbol,
    "interval":interval,
    "apikey":stock_price_api,
    "outputsize":"compact",
}

