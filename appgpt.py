from dotenv import load_dotenv
import os
import base64
import streamlit as st
import io
import pdfplumber
import openai

# Replace 'your-api-key' with your actual API key
openai.api_key = 'your-api-key'

def get_gpt3_response(input, pdf_content, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{input} {pdf_content} {prompt}"},
        ],
    )
    return response['choices'][0]['message']['content']

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to text
        with pdfplumber.open(uploaded_file) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
        return text

# Streamlit code
st.set_page_config(page_title="ATS Resume EXpert")
st.header("ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    pdf_content = input_pdf_setup(uploaded_file)

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    response = get_gpt3_response(input_text, pdf_content, input_prompt1)
    st.text_area('Response:', response, height=400)

if submit3:
    response = get_gpt3_response(input_text, pdf_content, input_prompt3)
    st.text_area('Response:', response, height=400)