import streamlit as st
import os

# Create the "claims" directory if it doesn't exist
if not os.path.exists("claims"):
    os.makedirs("claims")


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
tab1, tab2 = st.tabs(["Submit Claim", "Process Claim"])

with tab1:
    st.header("Submit Claim")
    uploaded_files = st.file_uploader("Upload Your Claim", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            save_uploaded_file(uploaded_file)

with tab2:
    st.header("Process Claim")
    st.write("This is where you can process claims.")

st.image("img/aniket_imginary_insurance.jpg", caption="Aniket Imaginary Insurance")


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