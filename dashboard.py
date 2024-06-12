import streamlit as st
import os

from pandasai.llm.local_llm import LocalLLM
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from pandasai import Agent
import main

from utils import DataFrameToCSVConverter

# Create the "claims" directory if it doesn't exist
if not os.path.exists("claims"):
    os.makedirs("claims")

load_dotenv()

def save_uploaded_file(uploaded_file):
    with open(os.path.join("claims", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success(f"Saved file: {uploaded_file.name}")


st.title("🛡️ Aniket Insurance Company Inc.")
st.markdown(
    """
    <div style='text-align: right;'>
        <h3>AI Process Your Claim</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Create tabs
tab1, tab2, tab3 = st.tabs(["Submit Claim", "Process Claim", "Claim Analysis"])

with tab1:
    st.header("Submit Claim")
    uploaded_files = st.file_uploader("Upload Your Claim", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            save_uploaded_file(uploaded_file)

with tab2:
    st.header("Process Claim")
    st.write("This is where you can process claims.")
    if st.button('Process'):
        main.process_claim()
        st.success('DataFrame has been written to claims_db/db.csv')

st.image("img/aniket_imginary_insurance.jpg", caption="Aniket Imaginary Insurance")

with tab3:
    st.header("Claim Analysis")
    st.write("Start Analyzing all claims.")
    model = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama3-70b-8192"
    )
    data = pd.read_csv('claims_db/db.csv')
    agent = Agent(data, config={"llm": model})
    prompt = st.text_input("What Analysis you like to run :")

    if st.button("Generate"):
        if prompt:
            with st.spinner("Generating response..."):
                response = agent.chat(prompt)
                print(response)
                if "temp_chart.png" in str(response):
                    st.image(response)
                else:
                    st.write(response)


# Add a footer with expander sections
st.markdown("---")

with st.expander("About Us"):
    st.write("Aniket Insurance Company Inc. is committed to providing excellent insurance services tailored to your needs. Our mission is to ensure your peace of mind through comprehensive coverage and exceptional customer service.")

with st.expander("Contact Us"):
    st.write("""
    **Email:** support@aniketImaginaryinsurance.com  
    **Phone:** +1 (123) 456-7890  
    **Address:** 123 Some Insurance St, Suite 100, Cityville, ST, 12345
    """)

with st.expander("Policies"):
    st.write("Our policies are designed to offer maximum protection and benefits to our customers. For more details, please visit our website or contact our support team.")