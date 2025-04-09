import streamlit as st
import ollama
import pdfplumber
import re

convo = []

# Function to interact with AI using Ollama Llama3.2
def stream_response(prompt):
    convo.append({'role': 'user', 'content': prompt})
    response = ''
    stream = ollama.chat(model='llama3.2', messages=convo, stream=True)
    for chunk in stream:
        response += chunk['message']['content']
        print(chunk['message']['content'], end='', flush=True)
    convo.append({'role': 'assistant', 'content': response})
    return response

# Function to extract text from a resume PDF
def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

# Function to rank candidates
def rank_candidate(resume_text, job_description):
    prompt = f"Rank the following resume against this job description.\nJob Description: {job_description}\nResume: {resume_text}"
    return stream_response(prompt)

# Function to suggest jobs based on resume content
def suggest_jobs(resume_text):
    prompt = f"Based on the following resume, suggest suitable job roles.\nResume: {resume_text}"
    return stream_response(prompt)

# Streamlit UI
st.title("Cost-Effective AI for Smart Job Matching Platforms")
st.header("NLP-Powered Resume Analysis and Job Recommendation")

# Step 1: Upload Resume
st.subheader("Step 1: Upload Resume (PDF)")
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
resume_text = ""
if uploaded_file is not None:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Resume Content:", resume_text, height=200)

# Step 2: Enter Job Description
st.subheader("Step 2: Enter Job Description")
job_description = st.text_area("Paste Job Description:")

# Step 3: Rank Candidate
if st.button("Rank Candidate"):
    if resume_text and job_description:
        st.write("**Candidate Ranking Result:**")
        st.write(rank_candidate(resume_text, job_description))
    else:
        st.error("Please upload a resume and enter a job description.")

# Step 4: Suggest Jobs Based on Resume
if st.button("Suggest Jobs"):
    if resume_text:
        st.write("**Suggested Job Roles:**")
        st.write(suggest_jobs(resume_text))
    else:
        st.error("Please upload a resume to get job suggestions.")
