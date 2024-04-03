from dotenv import load_dotenv
import os
import base64
import streamlit as st
import io
import pdfplumber
import openai
import gemini

# Replace 'your-api-key' with your actual API keys
openai.api_key = 'your-openai-api-key'
gemini.api_key = 'your-gemini-api-key'

def get_gpt3_response(input, pdf_content, prompt):
    #gpt
    pass

def get_gemini_response(input, pdf_content, prompt):
    #gemini
    pass

def input_pdf_setup(uploaded_file):
    #pdf
    pass

# Streamlit code
st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    pdf_content = input_pdf_setup(uploaded_file)

submit1 = st.button("Tell Me About the Resume")

if submit1:
    gpt3_response = get_gpt3_response(input_text, pdf_content, input_prompt1)
    gemini_response = get_gemini_response(input_text, pdf_content, input_prompt1)
    st.write("GPT-3 Response: ", gpt3_response)
    st.write("Gemini Response: ", gemini_response)