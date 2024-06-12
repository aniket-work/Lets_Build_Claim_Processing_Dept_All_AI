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
    # Specify the path to your PDF file
    filename = "claims/Aniket_Home_Company_Invoice.pdf"

    # Call the partition_pdf function
    # Returns a List[Element] present in the pages of the parsed pdf document
    elements = partition_pdf(filename)

    element_dict = [el.to_dict() for el in elements]
    output = json.dumps(element_dict, indent=2)
    print(output)

    unique_types = set(item['type'] for item in element_dict)
    print(unique_types)

    # Load the .env file
    load_dotenv(find_dotenv())
    free_api_key_auth = os.environ.get('free_api_key')

    client = UnstructuredClient(api_key_auth=free_api_key_auth)
    with open(filename, "rb") as f:
        files = shared.Files(content=f.read(), file_name=filename)

    req = shared.PartitionParameters(
        files=files,
        strategy="hi_res",
        hi_res_model_name="yolox",
        skip_infer_table_types=[],
        pdf_infer_table_structure=True,
    )

    try:
        resp = client.general.partition(req)
        elements = dict_to_elements(resp.elements)
    except SDKError as e:
        st.error(e)
        return

    tables = [el for el in elements if el.category == "Table"]
    if tables:
        table_html = tables[0].metadata.text_as_html
        parser = etree.XMLParser(remove_blank_text=True)
        file_obj = StringIO(table_html)
        tree = etree.parse(file_obj, parser)
        HTML(table_html)

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
        st.success('DataFrame has been written to claims_db/db.csv')

