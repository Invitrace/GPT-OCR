#global packages
import streamlit as st
import openai
import pytesseract

# local modules
from ocr_engine import image_to_script

#Setup Model
openai.api_key = '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'
ocr_engine = "pytesseract"

# Setup session state
st.title('OCR-GPT Model')
st.write('Best for English language and support both medical and general field')
st.file_uploader("Choose an image", key="img", type = ['png','jpeg','jpg'])

st.write(st.session_state.img)

if st.session_state['img'] is not None:
    img = st.session_state['img']
    st.text(type(img))
    st.image(img)
    
    # Save the uplaoded image as sample_0.jpg
    with open("samples/sample_0.jpg","wb") as f: 
      f.write(img.getbuffer())
    
    script, raw_ocr_output = image_to_script('samples/sample_0.jpg', ocr_engine , None, get_raw_ocr_text = True)
    st.text(script) # ผลลัพธ์ของ chatgpt