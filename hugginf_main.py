import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEndpoint

#os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN

st.title("HuggingFace Project")
st.write("HF:",HUGGINGFACEHUB_API_TOKEN)
