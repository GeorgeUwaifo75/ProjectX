import streamlit as st
import requests
import pandas as pd
import json
from dotenv import load_dotenv


coin = ""
user_question=""

def return_url(coin, COIN_API):
  return f"https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin}&tsym=USD&limit=10&api_key={COIN_API}"

def do_initApp():
  st.title("Short term Currency evaluation")

def handle_userinput(coin,COIN_API):
  # The API endpoint
  url =  return_url(coin,COIN_API)
  st.write(url)
  # A GET request to the API
  response = requests.get(url)

  df = pd.read_json(url)
  #st.write(df.head())


def main():
  load_dotenv()
  st.set_page_config(page_title="Short term Currency evaluation", page_icon=":books:")
    
  do_initApp()
  user_question = st.text_input("Ask a question about Crypto any coin:")

  # Ask a question
  if user_question:
      # st.write("Coin:",coin)
      handle_userinput(user_question,COIN_API)
    


if __name__ == '__main__':
    main()
