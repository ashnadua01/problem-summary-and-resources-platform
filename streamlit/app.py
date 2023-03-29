import os
import openai
import streamlit as st
import sys
sys.path.append('.')

from function.functions import summary, search

openai.api_key = os.getenv('OPENAI_KEY')

if "summary" not in st.session_state:
    st.session_state["summary"] = ""

st.title("Problem Summary and Resources")

input_text = st.text_area(label="Enter the Problem Statement", value="", height=150)
st.button("**Submit**",
          on_click=summary,
          kwargs={"text": input_text},
          )

st.write("\n")

output_text = st.text_area(label='Problem Summary', value=st.session_state["summary"], height=200)

if st.button("**Display Resources**"):
    search_results = search(input_text)
    for result in search_results:
        st.write(f"<h4>{result['title']}</h4>", unsafe_allow_html=True)
        st.write(result['link'])
        st.write(result['description'])

