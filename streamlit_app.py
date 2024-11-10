import streamlit as st
import pandas as pd
import time
from io import StringIO

from reply_machine import ReplyMachine, Sample
from chat import Chat


class Response:
    def __init__(self,
                 product_info_text,
                 lead_info_text,    
                 email_info_text):
        self.product_info_text = product_info_text
        self.lead_info_text = lead_info_text
        self.email_info_text = email_info_text

        self.sample = Sample()
        self.chat = Chat()

        self.R = ReplyMachine(
            product_information=product_info_text,
            email_content=email_info_text,
            chat=self.chat,
            lead_info=lead_info_text,
        )

    def generate_response(self, question):
        response = self.R.reply(question)
        print(response)
        return response
    
    def quick_bytes(self):
        if len(self.R.qa_threads) == 0:
            return "No Chat History Found"
        return self.R.quick_bytes()


product_info_text = None
lead_info_text = None
email_info_text = None


# Title of the app
st.title("Colca System - Automated AI QA")

st.markdown("---")
st.markdown('<h3 style="text-align: center;"> File Upload </h3>', unsafe_allow_html=True)


### Product Information
st.markdown("### Product Information")
product_option = st.radio("Choose input method", ("Upload a file", "Paste text"), key="product_option")

# Case 1: Upload a CSV file
if product_option == "Upload a file":
    uploaded_file = st.file_uploader("Choose a .txt file", type=".txt", key="product_file_uploader")
    if uploaded_file is not None:        
        product_info_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        product_info_text = st.text_area("Edit the Product Info Text : ", product_info_text, height=300, key="product_text_area")

# Case 2: Paste text directly into a text area
elif product_option == "Paste text":
    product_info_text = st.text_area("Paste your text here")
    if product_info_text:
        product_info_text = StringIO(product_info_text).read()
  

### Lead Information
st.markdown("### Lead Information")
lead_option = st.radio("Choose input method", ("Upload a file", "Paste text"), key="lead_info")

# Case 1: Upload a CSV file
if lead_option == "Upload a file":
    uploaded_file = st.file_uploader("Choose a .txt file", type=".txt", key="lead_file_uploaded")
    if uploaded_file is not None:        
        lead_info_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        lead_info_text = st.text_area("Edit the Lead Info Text : ", lead_info_text, height=300,  key="lead_text_area")

# Case 2: Paste text directly into a text area
elif lead_option == "Paste text":
    lead_info_text = st.text_area("Paste your text here")
    if lead_info_text:
        lead_info_text = StringIO(lead_info_text).read()

### Email Content Information
st.markdown("### Email Content")
email_option = st.radio("Choose input method", ("Upload a file", "Paste text"), key="email_info")

# Case 1: Upload a CSV file
if email_option == "Upload a file":
    uploaded_file = st.file_uploader("Choose a .txt file", type=".txt", key="email_file_uploaded")
    if uploaded_file is not None:        
        email_info_text = StringIO(uploaded_file.getvalue().decode("utf-8")).read()
        email_info_text = st.text_area("Edit the Email Content Text : ", email_info_text, height=300,  key="email_text_area")

# Case 2: Paste text directly into a text area
elif email_option == "Paste text":
    email_info_text = st.text_area("Paste your text here")
    if email_info_text:
        email_info_text = StringIO(email_info_text).read()

st.markdown("---")


####### QA system
if product_info_text and lead_info_text and email_info_text:
    print("-"*30, " INITIALIZED")
    if "__response" not in st.session_state:
        st.session_state.__response = Response(product_info_text=product_info_text,
                          lead_info_text=lead_info_text,
                          email_info_text=email_info_text
                          )    
    st.markdown('<h3 style="text-align: center;"> AI Question - Answer System </h3>', unsafe_allow_html=True)

    #### QA columns
    col1, col2 = st.columns(2)

    with col1:
        user_input = st.text_area("Ask your Question Here:", height=150, key="question")

    if st.button("Generate Response", key="generate_button"):
        response = st.session_state.__response.generate_response(user_input)
        quick_bytes = st.session_state.__response.quick_bytes()

        st.session_state.chat_input = response
        st.session_state.quick_bytes = quick_bytes


    with col2:
        if "chat_input" not in st.session_state:
            st.session_state.chat_input = ""

        st.text_area("AI Response", st.session_state.chat_input, height=150, disabled=True)

########### generate Quick bytes

    if "quick_bytes" not in st.session_state:
        st.session_state.quick_bytes = ""
    st.text_area("Quick Bytes", st.session_state.quick_bytes, height=300, disabled=True)


else:
    st.warning("Please upload or paste the information in all sections (Product Information, Lead Information, and Email Content) before proceeding.")


