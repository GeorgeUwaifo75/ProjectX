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
from finbert_utils import estimate_sentiment

from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

urls = ["https://decrypt.co/news", "https://www.coindesk.com/", "https://thecryptobasic.com/","https://cryptopotato.com/","https://u.today/"]
#arrx = ["BTC","Eth", "Sol"]

def return_url(coin, COIN_API):
  return f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin}&tsym=USD&limit=10&api_key={COIN_API}"

def do_initApp():
  st.title("Short term Currency evaluation")

def get_online_news(coin):
    text=""
    #Requesting website
    #url = "https://www.coindesk.com/"
    for x in urls:
          #response = requests.get(url)
          response = requests.get(x)
          st.write("Url:",x)
          
          if response.status_code == 200: #Check for successful response
              st.write("Coin:",coin)
              soup = BeautifulSoup(response.text, "html.parser")
              headlines = soup.find_all("h3")
              for headline in headlines:
                  if coin in headline.text.lower(): # Case-insensitive check
                      text+= headline.text+ ".\n"
                      
          else:
              print(f"Error: Request failed with status code {response.status_code}")
          
    return text
  

def get_sentiment(coin): 
  #today, three_days_prior = self.get_dates()
  #news = self.api.get_news(symbol=self.symbol, 
  #                             start=three_days_prior , 
  #                             end=today)
  #The section below uses the ev object to access the dictionary to get the ["Headline"] in News to create a List.
  #news = [ev.__dict__["_raw"]["headline"] for ev in news] 
 
  news = get_online_news((coin+" "))
  st.write("News: ",news)
  #news = "This coin has a lot of patronage at this time.  You should probably buy"
  
  probability, sentiment = estimate_sentiment(news)
    
  return probability, sentiment  



def handle_userinput(coin,COIN_API):
  # The API endpoint
  url =  return_url(coin,COIN_API)
  #st.write(url)
  # A GET request to the API
  response = requests.get(url)

  #st.write("Response:",response)
  
  
  df = pd.read_json(url)
  # Access the 'Data' array
  data_array = df['Data']['Data']
  
  df2 = pd.DataFrame(data_array)
 
  #st.write(df2.shape)

  # Iterate through the items in the 'Data' array
  #for item in data_array:
  #    # Process each item here
  #    st.write(item['time'], item['high'], item['low'], item['open'], item['volumefrom'], item['volumeto']) 

  pattn=""
  lowerV=0
  upperV=0
  percntg=0
  
  for x in (5,6,7,8,9,10):
    try:
        #st.write(f"X Value {x}:", df2['high'].iloc[x])
        if x>=5 and x<10:
          if x==8:
            lowerV=df2['high'].iloc[x]
         
          if df2['high'].iloc[x+1] >= df2['high'].iloc[x]:
            pattn +="U"
          else:
            pattn +="D"
        else:
          pattn+="-"
          upperV=df2['high'].iloc[x]
          
    except IndexError:
        st.write(f"Index {x} out of bounds.")
  
  #st.write("Pattern:",pattn)
  

  if lowerV > upperV:
    percntg= round( (100-((100/lowerV)*upperV)),2)
    st.write("percentage drop:",percntg,"%")
    if pattn[4]=='U' and percntg >= 3:
        st.write("With a percentage drop of 3% or above, you should buy if the sentiment is neutral or positive.")
    elif pattn[4]=='U' and percntg >= 1.5 and percntg < 3:
        st.write("The percentage drop of between 1.5% and 3%, you should buy if the sentiment is neutral or positive.")
    elif pattn[4]=='U' and percntg >= 0.5 and percntg < 1.5:
        st.write("The percentage drop of between 0.5% and 1.5%, you should buy if the sentiment positive.")
    elif pattn[4]=='D' and percntg >= 1.1 and percntg <= 2.0:
        st.write("There is a moderate percentage drop of between 1.1% and 2.0%, watch this asset for when it picks up.")
    elif pattn[4]=='D' and percntg > 2.0:
        st.write("There is has been a sharp percentage drop of over 2.0%, this might be an opportuned time to invest.")
  
  try:
      # Convert Unix timestamps to datetime objects
      df2['time'] = pd.to_datetime(df2['time'], unit='s')
  
      # Format the datetime objects to 'YYYY-mm-dd'
      df2['time'] = df2['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

  except (ValueError, TypeError) as e:
      st.error(f"Error converting timestamps: {e}")
      st.stop() #Stop execution if conversion fails

  df2 = df2.sort_values('time', ascending=True)

  #New addition
  # Find the index of 'high' in the DataFrame columns
  try:
    default_index = list(df2.columns).index('high')
  except ValueError:
    # Handle case where 'high' column doesn't exist.  Choose a default or handle the error appropriately
    default_index = 0  # Defaults to the first column if 'high' is missing.  You might want a more informative message here.
    st.warning("Column 'high' not found, defaulting to the first column.")
  column = st.selectbox('Select a column', df2.columns, index=default_index)

  
  #column = st.selectbox('Select a column', df2.columns)
  title = st.text_input('Title', 'Line Plot')
  x_label = st.text_input('X-axis Label', 'X-axis')
  y_label = st.text_input('Y-axis Label', column)   #
  color = st.color_picker('Line Color', '#1f77b4')

  fig, ax = plt.subplots()
  ax.plot(df2['time'], df2[column], color=color)
  ax.set_title(title)
  ax.set_xlabel(x_label)
  ax.set_ylabel(y_label)
  ax.grid()
  
  # Rotate X-axis labels
  plt.xticks(rotation=75)
  

  st.pyplot(fig)

 
#New addition ends


def main():
  coin = ""
  user_question=""
  COIN_API = os.environ.get("COIN_API")

  st.set_page_config(page_title="Short term Currency evaluation", page_icon=":books:")
    
  do_initApp()
  user_question = st.text_input("Ask a question about Crypto any coin:")

  # Ask a question
  if user_question:
      # st.write("Coin:",coin)
      handle_userinput(user_question,COIN_API)
      
      probability, sentiment = get_sentiment(user_question)
      
      st.write("Sentiment: ",sentiment)
      st.write("Probability: ",probability)
      if sentiment == "positive" and probability>.850:
        st.write("Go ahead and buy.")
      else:
        st.write("Don't buy yet!")
          
    


if __name__ == '__main__':
    main()
