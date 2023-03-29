import os
from googleapiclient.discovery import build
import spacy
import openai
import streamlit as st

def summary(text):
    updated_prompt = f"Give an easier explanation of this problem in words: {text}. Don't give code"
    st.session_state["summary"] = openai.Completion.create(
        model="text-davinci-003",
        prompt=updated_prompt,
        temperature=.5,
        max_tokens=1000,
    )["choices"][0]["text"]

def search(text):
    api_key = os.getenv('GOOGLE_API_KEY')
    cse_id = os.getenv('GOOGLE_CSE_ID')
    service = build("customsearch", "v1", developerKey=api_key)
    
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    keywords = []

    for token in doc:
        if not token.is_stop and not token.is_punct and token.text.strip():
            keywords.append(token.text)

    if len(keywords) == 0:
        return []
    else:
        query = ' '.join(keywords)
        query += ' problem solution'
        result = service.cse().list(q=query, cx=cse_id).execute()
        search_results = []
        for item in result['items']:
            search_results.append({
                'title': item['title'],
                'link': item['link'],
                'description': item['snippet']
            })
        return search_results
