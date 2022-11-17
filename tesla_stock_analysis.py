#Installing packages

!pip install yfinance==0.1.67
!pip install bs4==4.10.0 -y
!pip install nbformat==4.2.0
!pip install bs4==4.10.0 -y
!pip install html5lib==1.1 -y
!pip install lxml==4.6.4
#!pip install plotly==5.3.1

#Importing packages

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#Function for making graphs

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Using the Ticker function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is TSLA
tesla=yf.Ticker('TSLA')

#Using the ticker object and the function history extract stock information and save it in a dataframe named tesla_data. Set the period parameter to max so we get information for the maximum amount of time.
tesla_data =tesla.history(period='max')

#Reseting the index using the reset_index(inplace=True) function on the tesla_data DataFrame.
tesla_data.reset_index(inplace=True)

#Displaying the first five rows of the tesla_data dataframe using the head function.
tesla_data.head()

#Webscraping to Extract Tesla Revenue Data

#Using the requests library to download the webpage https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue. 
#Then saving the text of the response as a variable named html_data.

url="https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text

#Parsing the html data using beautiful_soup.

soup= BeautifulSoup (html_data, 'html.parser')

#Using BeautifulSoup or the read_html function extract the table with Tesla Quarterly Revenue and storing it into a dataframe named tesla_revenue. 

read_html_pandas_data = pd.read_html(url)
read_html_pandas_data = pd.read_html(str(soup))
tesla_revenue = read_html_pandas_data[1]

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in soup.find("tbody").find_all("tr"):
    col = row.find_all("td")
    date =col[0].text
    revenue =col[1].text
    
    tesla_revenue = tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)

#Removing the comma and dollar sign from the Revenue column.

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")

#Removing null or empty strings in the Revenue column.

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

#Displaying the last 5 row of the tesla_revenue dataframe using the tail function.
tesla_revenue.tail()

#Making Graph
make_graph(tesla_share_pricedata, tesla_revenue, 'Tesla')
