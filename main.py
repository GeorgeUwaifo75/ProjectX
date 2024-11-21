import streamlit as st
import requests
import pandas as pd
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
