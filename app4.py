import streamlit as st
import textwrap
import google.generativeai as genai
from googleapiclient.discovery import build
from PyPDF2 import PdfReader
import docx

# Function to convert text to markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf = PdfReader(pdf_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Function to perform Google Custom Search
def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

# Configure the Google Generative AI API key
genai.configure(api_key='AIzaSyB12Lm7FTjE61acrZF2qLKdLyHbAAmzi94')

# Define the model
model = genai.GenerativeModel('gemini-1.5-flash')

# Streamlit interface
st.image("hsbc_logo.jpg", width=150)
st.title("CARM Generator")

# User input for company name
user_input = st.text_input("Please enter the company name:")

# File uploader for PDF or Word documents
uploaded_file = st.file_uploader("Upload PDF or Word document", type=['pdf', 'docx'])

# Google Custom Search API credentials
google_api_key = 'AIzaSyDPqfK9wSIWRfiTxOg_NHmEVspw5XY_V4A'
google_cse_id = 'e72a23ae066f04d54'

if st.button("Generate Report"):
    if user_input:
        document_text = ""
        if uploaded_file:
            # Extract text from uploaded file
            if uploaded_file.type == "application/pdf":
                document_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                document_text = extract_text_from_docx(uploaded_file)
        
        # Perform Google search
        search_results = google_search(user_input, google_api_key, google_cse_id)
        search_text = "\n".join([result['snippet'] for result in search_results])
        
        # Create the prompt
        if document_text:
            prompt = f"Generate me a report that includes 1) Company background, 2) Business Segment, 3) Management Team , 4) Most Recent Financial Ratios (profitability, solvency, liquidity, etc) of the following company: {user_input}. Use your own knowledge, internet sources, and the following document: {document_text}. Additionally, include information from these search results: {search_text}"
        else:
            prompt = f"Generate me a report that includes 1) Company background, 2) Business Segment, 3) Management Team, 4) Most Recent Financial Ratios (profitability, solvency, liquidity, etc) of the following company: {user_input}. Use your own knowledge and internet sources. Additionally, include information from these search results: {search_text}"
        
        response = model.generate_content(prompt)
        
        # Display the response in a clear format
        st.markdown("### Generated Report")
        st.markdown(to_markdown(response.text))
    else:
        st.warning("Please enter a company name.")

# Replace 'YOUR_GOOGLE_SEARCH_API_KEY' and 'YOUR_CUSTOM_SEARCH_ENGINE_ID' with your actual credentials
