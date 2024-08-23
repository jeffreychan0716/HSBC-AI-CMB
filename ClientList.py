# Wrong code to deactivate it
import wrong code to deactivate it

import streamlit as st
import textwrap
import google.generativeai as genai
from googleapiclient.discovery import build
from PyPDF2 import PdfReader
import docx
from PIL import Image

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
# Load the logo image
logo = Image.open('hsbc_logo.jpg')

# Create a layout with the logo on the left
col1, col2 = st.columns([1, 3])

with col1:
    st.image(logo, use_column_width=True)

with col2:
    st.title("CMBFlash - Prospective Clients")

# User input for industry and regions
user_input_industry = st.text_input("Please enter the industry:", key='industry_input')
user_input_regions = st.text_input("Please enter the regions:", key='regions_input')

# File uploader for PDF or Word documents
uploaded_file = st.file_uploader("Upload PDF or Word document", type=['pdf', 'docx'])

# Google Custom Search API credentials
google_api_key = 'AIzaSyDPqfK9wSIWRfiTxOg_NHmEVspw5XY_V4A'
google_cse_id = 'e72a23ae066f04d54'

if st.button("Generate Report"):
    if user_input_industry and user_input_regions:
        document_text = ""
        if uploaded_file:
            # Extract text from uploaded file
            if uploaded_file.type == "application/pdf":
                document_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                document_text = extract_text_from_docx(uploaded_file)
        
        # Perform Google search
        search_results = google_search(user_input_industry, google_api_key, google_cse_id)
        search_text = "\n".join([result['snippet'] for result in search_results if 'snippet' in result])

        # Create the prompt
        if document_text:
            prompt = f"Generate me a report that includes 1) latest industry market trend with data in point form, 2) Profitability of the industry in table format, 3) Potential financial products HSBC can provide to companies in this industry with rationale in table format, 4) top 100 companies in the {user_input_industry} industry in table format (include chinese, english name, stock code if listed, market capitalization, revenue in USD, office headquarter, webiste, what business they are doing, business breakdown by region (make it up), contact person with their position (make it up if you have no information), phone number (make it up if you have no information)), based in {user_input_regions}. Add a line to separate each session. Use your own knowledge, internet sources, and the following document: {document_text}. Additionally, include information from these search results: {search_text}"
        else:
            prompt = f"Generate me a report that includes 1) latest industry market trend with data in point form, 2) Profitability of the industry in table format, 3) Potential financial products HSBC can provide to companies in this industry with rationale in table format, 4) top 100 companies in the {user_input_industry} industry in table format (include chinese, english name, stock code if listed, market capitalization, revenue in USD, office headquarter, webiste, what business they are doing, business breakdown by region (make it up), contact person with their position (make it up if you have no information), phone number (make it up if you have no information)), based in {user_input_regions}. Add a line to separate each session. Use your own knowledge and internet sources. Additionally, include information from these search results: {search_text}"
        
        response = model.generate_content(prompt)
        
        # Display the response in a clear format
        st.markdown("### Generated Report")
        st.markdown(to_markdown(response.text))
    else:
        st.warning("Please enter both the industry and the regions.")
