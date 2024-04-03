
from dotenv import load_dotenv

load_dotenv()
import fitz  # PyMuPDF
import base64
import streamlit as st
import os
import io
from PIL import Image
import pdf2image
import openai

# Configure the OpenAI API client
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_first_page(uploaded_file):
    """
    Extracts text from the first page of the uploaded PDF file.
    """
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        first_page_text = doc[0].get_text()
    return first_page_text


def get_gpt_response(prompt, pdf_content):
    response = openai.Completion.create(
        engine="text-davinci-003",  # You can choose the engine you prefer
        prompt=prompt,
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # In this OpenAI version, we do not send the PDF content to the API.
        # So, this function does not need to return pdf_parts anymore.
        return base64.b64encode(img_byte_arr).decode()  # encode to base64
    else:
        raise FileNotFoundError("No file uploaded")

## Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """Your task is to review the provided resume against the job description..."""

input_prompt3 = """Your task is to evaluate the resume against the provided job description..."""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)  # Note: The PDF content is not directly used in GPT prompt
        response = get_gpt_response(input_prompt1, pdf_content)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)  # Note: The PDF content is not directly used
