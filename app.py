import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. Page Config
st.set_page_config(page_title="Insurance Lead Tracker", page_icon="🛡️")

# This code hides the Streamlit footer and the "Made with Streamlit" brand
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stAppToolbar {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

def get_gspread_client():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        info = dict(st.secrets["gcp_service_account"])
        # Fix formatting for Google Library
        info["private_key"] = info["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(info, scopes=scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Secret Loading Error: {e}")
        return None

st.title("🛡️ Personal Risk Protection Analyzer")

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
    types = st.multiselect("Interests", ["Life", "Income Protection", "Trauma", "TPD", "Health", "Car", "Home", "Content"])
    notes = st.text_area("Notes for Advisor")
    
    if st.form_submit_button("Submit to Lead Tracker"):
        if name and email:
            client = get_gspread_client()
            if client:
                try:
                    # Your Specific Sheet ID
                    sheet = client.open_by_key("1V0emFdEceVa3JB5uctCw5PMYC-li_YvbZZFQmQwj0vI").sheet1
                    
                    # FIXED COLUMN ORDER:
                    # A:Name, B:Email, C:Phone, D:Age, E:Status, F:Types, G:Spacer, H:Mortgage, I:Income, J:Notes
                    new_row = [name, email, phone, age, status, ", ".join(types), "N/A", m_pay, a_inc, notes]
                    
                    sheet.append_row(new_row)
                    st.success("✅ Lead saved! Advisor will contact you shortly.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Sheet Error: {e}")
        else:
            st.warning("Please enter name and email.")
