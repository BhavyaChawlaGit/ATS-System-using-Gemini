#from dotenv import load_dotenv
import os
import base64
import streamlit as st
import io
import pdfplumber
import openai

# Replace 'your-api-key' with your actual API key
#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = st.secrets["OPENAI_API_KEY"]

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
st.set_page_config(page_title="Resume Expert")
st.header("ResumeRight - ATS System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    pdf_content = input_pdf_setup(uploaded_file)
else:
    pdf_content = None

submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improvise my Resume")
submit3 = st.button("Percentage Match")
submit4 = st.button("Cover Letter")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""


input_prompt2 = """
You are an experienced Human Resource Manager, your task is to review the provided resume against the job description.
Please provide feedback on how the candidate can improve their resume to better align with the job requirements.
In the ouput highlight the areas that need improvement and suggest changes or an updated resume to enhance the candidate's profile per the job description.
Do not add any information which is not present in the resume, Also make a verification check whether the attached data is 
"""


input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing in bullet points and last final thoughts. 
Please make sure the output is clear and concise for the applicant to understand.
"""

input_prompt4 = """
You are an experienced Human Resource Manager, your task is to review the provided resume against the job description.
Please provide a cover letter for the candidate that aligns with the job requirements.
In the output, provide a cover letter that highlights the candidate's skills and experiences that are relevant to the job description using the Resume.
Make sure it is professional and engaging to the employer and increases the candidate's chances of getting an interview.
It should be 200-400 words long. Do not include dates or addresses in the cover letter. Try to add extraco-curricular activities and hobbies from resume if available.
and which are relevant.
"""


if not input_text:
        st.error("Please enter job description/requirements.")
elif not pdf_content:
        st.error("Please upload a PDF.")
else:
    if submit1:
        response = get_gpt3_response(input_text, pdf_content, input_prompt1)
        st.text_area('Response:', response, height=500)
    elif submit2:
        response = get_gpt3_response(input_text, pdf_content, input_prompt2)
        st.text_area('Response:', response, height=500)
    elif submit3:
        response = get_gpt3_response(input_text, pdf_content, input_prompt3)
        st.text_area('Response:', response, height=500)
    elif submit4:
        response = get_gpt3_response(input_text, pdf_content, input_prompt4)
        st.text_area('Response:', response, height=500)