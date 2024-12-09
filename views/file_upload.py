import os
import streamlit as st
import time
import base64
from google.oauth2 import service_account
from google.cloud import documentai_v1 as documentai
import base64
import vertexai
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
    Part,
)


def save_uploaded_file(uploadedfile):
  with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
     f.write(uploadedfile.getbuffer())
  return st.success("Saved file :{} in tempDir".format(uploadedfile.name))

credentials = service_account.Credentials.from_service_account_file('/Users/haroonshoaib/Downloads/nlpanomalydet-21686a781d06.json')
project_id = "nlpanomalydet"
location = "us"  # Choose your location (e.g., "us" or "eu")
processor_id = "96ec437057e85de8"  # The ID of your Document AI processor

# Initialize Document AI client
client = documentai.DocumentProcessorServiceClient(credentials=credentials)

def process_document(fileup):
    # Read the file as binary
    #with open(file_path, "rb") as file:
     #   file_content = file.read()
    
    # Configure the document type and content
    document = {"content": fileup, "mime_type": "application/pdf"}  # or "image/jpeg" for images
    
    # Configure the request
    request = {
        "name": f"projects/{project_id}/locations/{location}/processors/{processor_id}",
        "raw_document": document,
    }
    
    # Process the document
    result = client.process_document(request=request)
    
    # Extract and print the text from the Document AI output
    document_text = result.document.text
    print("Extracted Text:", document_text)
    return document_text

vertexai.init(project="nlpanomalydet", location="us-central1")

def analyze_pdf_handwriting(pdf_bytes):
    """
    Analyze handwriting in a PDF document
    
    Args:
        pdf_doc (str): Local path to the PDF file
    """
    # Read PDF file as bytes and encode to base64
    #with open(pdf_doc, 'rb') as pdf_file:
        #pdf_bytes = pdf_file.read()
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    
    # Create a Part from the base64 encoded PDF
    pdf_part = Part.from_data(
        data=pdf_base64, 
        mime_type="application/pdf"
    )

    # Detailed prompt for handwriting analysis
    prompt = """
    Comprehensive Handwriting Analysis for Multi-Writer Detection:

    Detailed Analytical Framework:
    1. Writer Identification
       - Determine total number of potential distinct writers
       - Identify page-by-page writing variations
    
    2. Handwriting Characteristic Analysis
       - Letter formation consistency
       - Stroke angle variations
       - Word spacing patterns
       - Pressure and pen/pencil stroke characteristics
       - Baseline consistency
       - Letter size and proportionality
    
    3. Transition Detection
       - Identify potential writer transition points
       - Highlight substantive handwriting style changes
    
    Analysis Requirements:
    - Provide quantitative evidence for writer distinctions
    - Use a systematic, forensic-like approach
    - Compare and contrast writing characteristics across document
    - May or may not have multiple authors
    
    Output Structure:
    - More than one writer: [Yes/No]
    - Estimated Number of Writers: [1/2]
    
    """

    # Initialize Gemini model
    model = GenerativeModel("gemini-1.5-pro-002")

    # Prepare contents
    contents = [prompt, pdf_part]

    # Generate analysis
    try:
        # Configure generation settings for more detailed output
        generation_config = GenerationConfig(
            temperature=0.2,
            max_output_tokens=4096
        )
        
        response = model.generate_content(
            contents, 
            generation_config=generation_config
        )
        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")

if "ans_sheet" not in st.session_state:
    st.session_state['ans_sheet'] = 'not done'

col1,col2 = st.columns(2)

def change_ans_sheet_state():
    st.session_state['ans_sheet'] = 'done'

col1.markdown(' ## Upload Answer Sheet')
uploaded_file = col1.file_uploader('UPLOAD PDF', type="pdf", on_change = change_ans_sheet_state)
if st.session_state['ans_sheet'] == 'done':
    progress_bar = col1.progress(0)

    for perc_comp in range(100):
        time.sleep(0.005)
        progress_bar.progress(perc_comp+1)
    col1.write("--")
    col1.success('Answer sheet uploaded successfully')
#if uploaded_file is not None:
#   df = extract_data(uploaded_file)


if uploaded_file is not None:
    
    base64_pdf = base64.b64encode(uploaded_file.read()).decode("utf-8")

    
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type}
    # Apply Function here
    #save_uploaded_file(uploaded_file)
    if 'semtext' not in st.session_state:
        st.session_state['semtext'] = process_document(uploaded_file.getvalue())
    if 'handtext' not in st.session_state:
        st.session_state['handtext'] = analyze_pdf_handwriting(uploaded_file.getvalue())
    #text = process_document(uploaded_file.getvalue())
        # html_str = f"""
        # <style>
        # p.a {{
        # font: bold 20px Courier;
        # }}
        # </style>
        # <p class="a">{st.session_state['handtext']}</p>
        #"""

    col2.markdown("## Handwriting Analysis Result:")
    

#st.markdown(html_str, unsafe_allow_html=True)
    col2.markdown(st.session_state['handtext'] )
# Example usage
#file_path = "/Users/haroonshoaib/Downloads/Assignment3.pdf"