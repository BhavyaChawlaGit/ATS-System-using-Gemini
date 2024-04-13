#from dotenv import load_dotenv
import os
import base64
import streamlit as st
import io
import pdfplumber
import openai
import docx
import psycopg2



# Replace 'your-api-key' with your actual API key
#openai.api_key = "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"
openai.api_key = st.secrets["OPENAI_API_KEY"]



def get_gpt3_response(input, pdf_content, prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a smart assistant to career advisors at the Harvard Extension School. Your take is to write Cover letters to be more brief and convincing according to the Resumes and Cover Letters guide."},
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

st.set_page_config(
        page_title="ResumeRight",
        # page_icon=":document:",
        layout="wide",
        initial_sidebar_state="auto",
    )


st.markdown(
    """
    # ResumeRight
    [![LinkedIn](https://img.shields.io/badge/LinkedIn-Visit-blue)](https://www.linkedin.com/in/bhavyachawla/)
    [![GitHub](https://img.shields.io/badge/GitHub-Visit-blue)](https://github.com/BhavyaChawlaGit)
    
    """,
    unsafe_allow_html=True,
)

st.markdown(
        "Welcome to ResumeRight! Drop JobDescription and your Resume below, and let us analyze it for you"
    )


input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")
    #Postgre connection and execution 
    
    # file_data = uploaded_file.read()
    
    # pdf_content = input_pdf_setup(io.BytesIO(file_data))
    
    pdf_content=input_pdf_setup(uploaded_file)
    
    
    

    # conn = psycopg2.connect(dbname="Resume", user="postgres", password="bhavyachawla", host="localhost")
    # cur = conn.cursor()

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS resumes (
    #         id SERIAL PRIMARY KEY,
    #         pdf_data BYTEA
    #     )
    # """)




    # cur.execute("INSERT INTO resumes (pdf_data) VALUES (%s)", (psycopg2.Binary(file_data),))

    # # Close communication with the database
    # conn.commit()
    # cur.close()
    # conn.close()

    # st.write(file_data)

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
You are a smart assistant to career advisors at the Harvard Extension School. Your take is to write a cover letter to be more brief and convincing according to the Resumes and Cover Letters guide. your task is to review and write a CV against the given Resume and job description.
It should be 300-500 words long. Do not include dates or addresses in the cover letter. and follow below guidelines.

Your task is to write the CV. Follow these guidelines:
- Be truthful and objective to the experience listed in the CV
- Be specific rather than general
- write job highlight items using STAR methodology (but do not mention STAR explicitly)
- Fix spelling and grammar errors
- Writte to express not impress
- Articulate and don't be flowery
- Prefer active voice over passive voice
- Do not include a summary about the candidate

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
        
        if submit4:

            
            response = get_gpt3_response(input_text, pdf_content, input_prompt4)
            doc = docx.Document()
            doc.add_paragraph(response)
            doc.save("CoverLetter.docx")
            
            st.success("Your cover letter is ready for download!")
            

            # Read the contents of the file
            with open("CoverLetter.docx", "rb") as file:
                file_data = file.read()

        
            # Create a download button for the file
            st.download_button(
                label="Download the generated cover letter",
                data=file_data,
                file_name="CoverLetter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            st.text_area('Response:', response, height=500)



