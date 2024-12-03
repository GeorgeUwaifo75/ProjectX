import os
import streamlit as st
import requests
import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import time
from scipy import stats
from sklearn import linear_model
#from finbert_utils import estimate_sentiment

#from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()
COIN_API = os.environ.get("COIN_API")


#COIN_API=""
#urls = ["https://decrypt.co/news", "https://www.coindesk.com/", "https://thecryptobasic.com/","https://cryptopotato.com/","https://u.today/"]
arrx = ["BTC","Eth","Sol","wld","DOGE","Pepe","Ada","Trx","Ton","Xmr"]

def return_url(coin, COIN_API):
  #st.write(f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin}&tsym=USD&limit=10&api_key={COIN_API}")
  return f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin}&tsym=USD&limit=10&api_key={COIN_API}"

def do_initApp():
  st.title("Dashboard Visual for all coins")

def create_arrays_plots():
  indx =0
  for coin in arrx:
    #st.write("Coin_Api:",COIN_API)
    #st.write("Coin:",coin)
    indx += 1
    st.write("indx:",indx)
    handle_userinput(coin,COIN_API,indx)
    
    

def handle_userinput(coin,COIN_API,indx):
  # The API endpoint
  url =  return_url(coin,COIN_API)
 
  # A GET request to the API
  response = requests.get(url)

  #st.write("Response:",response)
  
  df = pd.read_json(url)
  # Access the 'Data' array
  data_array = df['Data']['Data']
  
  df2 = pd.DataFrame(data_array)
 

  try:
      # Convert Unix timestamps to datetime objects
      df2['time'] = pd.to_datetime(df2['time'], unit='s')
  
      # Format the datetime objects to 'YYYY-mm-dd'
      df2['time'] = df2['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

  except (ValueError, TypeError) as e:
      st.error(f"Error converting timestamps: {e}")
      st.stop() #Stop execution if conversion fails

  df2 = df2.sort_values('time', ascending=True)

  # Find the index of 'high' in the DataFrame columns
  try:
    default_index = list(df2.columns).index('high')
  except ValueError:
    # Handle case where 'high' column doesn't exist.  Choose a default or handle the error appropriately
    default_index = 0  # Defaults to the first column if 'high' is missing.  You might want a more informative message here.
    st.warning("Column 'high' not found, defaulting to the first column.")
  
  column = coin
  st.write("Coin:",coin)
  
  
  #fig, ax = plt.subplots()
  #ax.plot(df2['time'], df2['high'], color='r')
  #ax.set_title("Coin Label")
  #ax.set_xlabel("x_label")
  #ax.set_ylabel("y_label")

  # Rotate X-axis labels
  #plt.xticks(rotation=45)

  #st.pyplot(fig)

  plt.subplot(5, 2, indx)
  plt.plot(df2['time'], df2['high'], color='r')

  plt.show()


def main():
  coin = ""
  user_question=""
  #COIN_API = os.environ.get("COIN_API")

  st.set_page_config(page_title="DashBoard for Coins", page_icon=":books:")
    
  do_initApp()
  create_arrays_plots()
    


if __name__ == '__main__':
    main()
