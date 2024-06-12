import warnings
import streamlit as st
import json
import os
from io import StringIO
from lxml import etree
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import dict_to_elements
from IPython.display import JSON
from IPython.core.display import HTML
from langchain_community.chat_models import ChatOllama
from langchain_core.documents import Document
from langchain.chains.summarize import load_summarize_chain
from utils import DataFrameToCSVConverter

warnings.filterwarnings('ignore')

def process_claim():
    """
    Processes a claim from a PDF file by extracting and summarizing its contents.

    This function performs the following steps:
    1. Reads a PDF file containing a claim.
    2. Extracts elements from the PDF using the partition_pdf function.
    3. Sends the extracted elements to an external service for further processing.
    4. Summarizes the contents of any tables found in the PDF.
    5. Converts the summarized table to a CSV file.
    6. Displays the processing status in the Streamlit app.
    """
    # Specify the path to your PDF file
    filename = "claims/Aniket_Home_Company_Invoice.pdf"

    # Call the partition_pdf function to extract elements from the PDF
    elements = partition_pdf(filename)

    # Convert elements to dictionaries for JSON output
    element_dict = [el.to_dict() for el in elements]
    output = json.dumps(element_dict, indent=2)
    print(output)

    # Get unique types of elements found in the PDF
    unique_types = set(item['type'] for item in element_dict)
    print(unique_types)

    # Load the .env file to get environment variables
    load_dotenv(find_dotenv())
    free_api_key_auth = os.environ.get('free_api_key')

    # Initialize the UnstructuredClient with the API key
    client = UnstructuredClient(api_key_auth=free_api_key_auth)
    with open(filename, "rb") as f:
        files = shared.Files(content=f.read(), file_name=filename)

    # Set up request parameters for the partitioning service
    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
        hi_res_model_name="yolox",
        skip_infer_table_types=[],
        pdf_infer_table_structure=True,
    )

    try:
        # Send request to the partitioning service and get response elements
        resp = client.general.partition(req)
        elements = dict_to_elements(resp.elements)
    except SDKError as e:
        # Display error message in Streamlit app if SDKError occurs
        st.error(e)
        return

    # Filter for table elements from the response
    tables = [el for el in elements if el.category == "Table"]
    if tables:
        table_html = tables[0].metadata.text_as_html
        parser = etree.XMLParser(remove_blank_text=True)
        file_obj = StringIO(table_html)
        tree = etree.parse(file_obj, parser)
        HTML(table_html)

        # Initialize ChatOllama model and load summarization chain
        llm = ChatOllama(model="llama3")
        chain = load_summarize_chain(llm, chain_type="stuff")
        output = chain.invoke([Document(page_content=table_html)])

        print(output['output_text'])

        # Convert HTML table to pandas DataFrame
        dfs = pd.read_html(table_html)
        df = dfs[0]

        print(df)
        print(df.head())

        # Convert the DataFrame to CSV
        DataFrameToCSVConverter.to_csv(df, 'claims_db/db.csv')
        st.success('Claim Processing Has Been Submitted.')
