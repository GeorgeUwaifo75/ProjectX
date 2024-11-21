import streamlit as st
import requests
import pandas as pd
import json
from dotenv import load_dotenv



def do_initApp():
  st.title("Short term Currency evaluation")

def handle_userinput(coin):
  # The API endpoint
  st.write("Coin:",coin)
  url =  "https://min-api.cryptocompare.com/data/v2/histohour?fsym={coin}&tsym=USD&limit=10&api_key={COIN_API}";

  # A GET request to the API
  response = requests.get(url)

  df = pd.read_json(url)


def main():
  load_dotenv()
  st.set_page_config(page_title="Short term Currency evaluation", page_icon=":books:")
    
  do_initApp()
  user_question = st.text_input("Ask a question about Crypto any coin:")

  # Ask a question
  if user_question:
      handle_userinput(user_question)
    


if __name__ == '__main__':
    main()
