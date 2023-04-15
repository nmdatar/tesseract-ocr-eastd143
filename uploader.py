import streamlit as st
import pandas as pd
import pytesseract
from typing import List, Tuple
from io import BytesIO
from PIL import Image

tesseract_codes = {
    'Chinese (Simplified)' : 'chi_sim',
    'Chinese (Traditional)' : 'chi_tra',
    'English' : 'eng',
    'Japanese' : 'jpn',
    'Korean' : 'kor',
    'Vietnamese' : 'vie',
    'Filipino (old-Tagalog)' : 'fil',
}

def extract_text(files: List = [], languages: List[str] = []) -> None:
    # pytesseract.pytesseract.tesseract_cmd = r"/usr/local/python/3.10.4/lib/python3.10/site-packages/tesseract"
    languages = [tesseract_codes[lang] for lang in languages]
    formatted_languages = "+".join(languages)
    
    display = pd.DataFrame(columns=['file_name', 'extracted_text'])
  
    for file in files:
        file_bytes = BytesIO(file.getvalue())
        file_image = Image.open(file_bytes)
        extracted_text = pytesseract.image_to_string(image=file_image, lang=formatted_languages)
        pd.concat([display, pd.DataFrame({'file_name': [file.name], 'extracted_text': [extracted_text]}, index=pd.RangeIndex(len(display), len(display)+1))], ignore_index=True, axis=0)


    st.dataframe(display)

    download_display_data = display.to_csv(index=False).encode('utf-8')

    st.download_button(
    label="Download data as CSV",
    data=download_display_data,
    file_name='ocr_extraction.csv',
    mime='text/csv',
)

if __name__ == '__main__':

    uploaded_files = st.file_uploader(label="Choose a file", accept_multiple_files=True, type=['png', 'jpg'])
    if uploaded_files is not None:

        options = st.multiselect(
        'Select a language or multiple to perform OCR on!',
        ['English', 'Chinese (Simplified)', 'Japanese', 'Korean', 'Vietnamese', 'Filipino (old-Tagalog)', 'Chinese (Traditional)'],
        ['English'])

        st.button('Initiate the OCR :)', on_click=extract_text, args=(uploaded_files, options))
