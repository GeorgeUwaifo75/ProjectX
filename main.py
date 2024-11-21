import streamlit as st
import requests
import pandas as pd
import json
from dotenv import load_dotenv


# The API endpoint
url =  "https://min-api.cryptocompare.com/data/v2/histohour?fsym=ETH&tsym=USD&limit=10&api_key=f40243a801d1e370c14f7fa36a71cab5cce7c1c035e9551fc7a0592901f3ea53";

# A GET request to the API
response = requests.get(url)

df = pd.read_json(url)

def do_initApp():
  st.title("Short term Currency evaluation")

def main():
  load_dotenv()
  st.set_page_config(page_title="Short term Currency evaluation", page_icon=":books:")
    
  do_initApp()


if __name__ == '__main__':
    main()
