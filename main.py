import warnings
warnings.filterwarnings('ignore')
from IPython.display import JSON

import json

from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError

from unstructured.partition.html import partition_html
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import dict_to_elements, elements_to_json
from unstructured.partition.pdf import partition_pdf

# Specify the path to your PDF file
filename = "claims/gpt4all.pdf"

# Call the partition_pdf function
# Returns a List[Element] present in the pages of the parsed pdf document
elements = partition_pdf(filename)


element_dict = [el.to_dict() for el in elements]
output = json.dumps(element_dict, indent=2)
print(output)

unique_types = set()

for item in element_dict:
    unique_types.add(item['type'])

print(unique_types)

import os
from dotenv import load_dotenv, find_dotenv

# Load the .env file
load_dotenv(find_dotenv())

free_api_key_auth = os.environ.get('free_api_key_auth')

client = UnstructuredClient(
    api_key_auth=free_api_key_auth
)

with open(filename, "rb") as f:
    files=shared.Files(
        content=f.read(),
        file_name=filename,
    )

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
    print(e)

tables = [el for el in elements if el.category == "Table"]


