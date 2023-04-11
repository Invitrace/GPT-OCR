#global packages
import streamlit as st
import openai
import pytesseract
import os
import json

# local modulesP
from ocr_engine import image_to_script

#Setup Model
## Design for streamlit
try:
  openai.api_key = os.environ['OPENAI-API-KEY']
## Design for local run
except KeyError:
  from dotenv import load_dotenv
  load_dotenv()
  api_key = os.getenv('OPENAI-API-KEY')
  openai.api_key = api_key

ocr_engine = "pytesseract"

# Setup session state
st.title('OCR-GPT Model')
st.write('Best for English language and support both medical and general field')
st.file_uploader("Choose an image", key="img", type = ['png','jpeg','jpg'])

st.write(st.session_state.img)

if st.session_state['img'] is not None:
    img = st.session_state['img']
    st.image(img)
    
    # Save the uplaoded image as sample_0.jpg
    with open("samples/sample_0.jpg","wb") as f: 
      f.write(img.getbuffer())
    
    with st.spinner('Waiting for it..'):
      script, raw_ocr_output = image_to_script('samples/sample_0.jpg', ocr_engine , None, get_raw_ocr_text = True)
      st.title('Output :')
      st.text(script) # ผลลัพธ์ของ chatgpt
      st.title('Raw (No correction) :')
      st.text(raw_ocr_output)
