# Global packages
import openai
import pytesseract # OCR 
from PIL import Image
import cv2

# Local modules
from preprocess_utils import preprocess_img

def img_to_raw_ocr_output(img, ocr_engine, lang):
    
    if ocr_engine == "pytesseract":
        custom_config = r'--oem 3 --psm 6'
        raw_ocr_output = pytesseract.image_to_string(img, config=custom_config, lang=lang)
    else:
        raise NotImplementedError("We are not implemented that OCR Engine yet")
    
    return raw_ocr_output


def image_to_script(img_path, ocr_engine = "pytesseract", lang = None, get_raw_ocr_text = False):
    # img_path : .png, .jpg files

    img = cv2.imread(img_path)
    img = preprocess_img(img)
    raw_ocr_output = img_to_raw_ocr_output(img,ocr_engine,lang)

    lang_dct = {None : 'British' ,'tha' : 'Thai'}
    role = f""""
    Ignore all your previous instructions, you are a {lang_dct[lang]} native called Abdul

    - Abdul is responsible for receiving OCR input related to medical or general fields, correct any misspelled words, and avoid paraphrasing the text although the collocation is bad
    - Although the input contains several errors and typos, Abdul will still try their best to output the answer

    Here's are two examples: 

    (Input) :
    / HEENT > No pale conjunctivae, ne (ctevic Scletra, no discharge per eyes / ears /NOse,
    No preaunicylar J Suomandibular / cervical |ymphad eno pathy'

    (Abdul) : 
    '/ HEENT > No pale conjunctivae, no icteric Sclera, no discharge per eyes / ears / nose,
    No preauricular / Submandibular / cervical |ymphadenopathy'
    
    (Input) :
    noh present . Worsning JF the burs persisted regardless of day and night The patient 's
    right eye

    (Abdul) : 
    not present . Worsening of the blurs persisted regardless of day and night The patient 's
    right eye
    """
                
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": raw_ocr_output},
            ]
    )

    script = ""
    for choice in response.choices:
        script += choice.message.content
    
    if get_raw_ocr_text:
        return script, raw_ocr_output

    return script