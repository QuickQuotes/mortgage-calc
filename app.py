import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Insurance Risk Lead Tracker", page_icon="🛡️")

# 2. Secure Connection Logic (The Fixed Function)
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # This version handles "escaped" characters much better
    info = dict(st.secrets["gcp_service_account"])
    
    # Clean the key: remove literal backslashes and fix newlines
    raw_key = info["private_key"]
    processed_key = raw_key.replace("\\n", "\n")
    info["private_key"] = processed_key
    
    creds = Credentials.from_service_account_info(info, scopes=scope)
    return gspread.authorize(creds)

# 3. The App UI
st.title("🛡️ Personal Risk Protection Analyzer")
st.write("Calculate your protection needs and request a specialist review.")

with st.expander("📊 Quick Estimate", expanded=True):
    m_pay = st.number_input("Monthly Mortgage ($)", value=3000)
    a_inc = st.number_input("Annual Income ($)", value=100000)
    rec_benefit = max(m_pay * 1.15, (a_inc * 0.45) / 12)
    st.info(f"Recommended Monthly Benefit: ${rec_benefit:,.2f}")

with st.form("lead_form", clear_on_submit=True):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    age = st.number_input("Age", value=30)
    status = st.selectbox("Current Cover", ["No existing cover", "Partial", "Fully covered"])
    types = st.multiselect("Interests", ["Life", "Income Protection", "Trauma", "TPD", "Health"])
    notes = st.text_area("Notes for Aman")
    
    if st.form_submit_button("Submit to Lead Tracker"):
        if name and email:
            try:
                client = get_gspread_client()
                # Replace the string below with your actual Sheet ID from the URL
                sheet = client.open_by_key("1V0emFdEceVa3JB5uctCw5PMYC-li_YvbZZFQmQwj0vI").sheet1
                
                new_row = [name, email, phone, age, status, ", ".join(types), m_pay, a_inc, notes]
                sheet.append_row(new_row)
                
                st.success("✅ Lead saved! Aman will contact you shortly.")
                st.balloons()
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter name and email.")
