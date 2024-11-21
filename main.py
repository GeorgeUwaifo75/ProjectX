import streamlit as st
import requests
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from scipy import stats
from sklearn import linear_model


import json
from dotenv import load_dotenv
load_dotenv()

def return_url(coin, COIN_API):
  return f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin}&tsym=USD&limit=10&api_key=f40243a801d1e370c14f7fa36a71cab5cce7c1c035e9551fc7a0592901f3ea53"

def do_initApp():
  st.title("Short term Currency evaluation")

def handle_userinput(coin,COIN_API):
  # The API endpoint
  url =  return_url(coin,COIN_API)
  st.write(url)
  # A GET request to the API
  response = requests.get(url)

  df = pd.read_json(url)
  # Access the 'Data' array
  data_array = df['Data']['Data']
  
  df2 = pd.DataFrame(data_array)
 
  st.write(df2.shape)

  # Iterate through the items in the 'Data' array
  #for item in data_array:
  #    # Process each item here
  #    st.write(item['time'], item['high'], item['low'], item['open'], item['volumefrom'], item['volumeto']) 

  #df2 = df2.sort_values('time', ascending=True)

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
  y_label = st.text_input('Y-axis Label', str(df2[column]))   #
  color = st.color_picker('Line Color', '#1f77b4')

  fig, ax = plt.subplots()
  ax.plot(df2['time'], df2[column], color=color)
  ax.set_title(title)
  ax.set_xlabel(x_label)
  ax.set_ylabel(y_label)

  # Rotate X-axis labels
  plt.xticks(rotation=45)

  st.pyplot(fig)
#New addition ends


def main():
  coin = ""
  user_question=""
  COIN_API=""

  st.set_page_config(page_title="Short term Currency evaluation", page_icon=":books:")
    
  do_initApp()
  user_question = st.text_input("Ask a question about Crypto any coin:")

  # Ask a question
  if user_question:
      # st.write("Coin:",coin)
      handle_userinput(user_question,COIN_API)
    


if __name__ == '__main__':
    main()
