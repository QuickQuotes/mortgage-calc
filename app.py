import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. Page Config
st.set_page_config(page_title="Insurance Lead Tracker", page_icon="🛡️")

# 2. All-in-One Styling (The fix for highlights and indentation)
st.markdown(
    """
    <style>
   /* 1. HIDE ALL BRANDING AND USERNAME AVATAR */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppToolbar {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    
    /* Targets the username, avatar, and 'Hosted' bar in the bottom right */
    div[class^="viewerBadge"], 
    div[class*="viewerBadge"],
    .st-emotion-cache-1vt458s,
    #viewer-badge-container {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
    }

    /* BACKGROUND GRADIENT */
    .stApp {
        background: linear-gradient(135deg, #49C6D6, #95C2C7);
        background-attachment: fixed;
    }

    /* THE HIGHLIGHT KILLER: This stops the white boxes around text */
    div[data-testid="stWidgetLabel"] div, 
    div[data-testid="stWidgetLabel"] p,
    .stMarkdown div, 
    .stMarkdown p,
    label p,
    span p {
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }

    /* TEXT COLOR: Pure Black */
    .stMarkdown, label, p, .stAlert, .stSelectbox label, .stMultiSelect label {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* SINGLE LINE TITLE */
    .title-text {
        white-space: nowrap;
        font-size: 2.1rem !important;
        font-weight: 700;
        color: #000000;
        text-align: center;
        padding: 10px 0px;
        margin-top: -40px;
    }
    </style>
    <h1 class="title-text">🛡️ Personal Risk Protection Analyzer</h1>
    """,
    unsafe_allow_html=True
)

def get_gspread_client():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        info = dict(st.secrets["gcp_service_account"])
        info["private_key"] = info["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(info, scopes=scope)
        return gspread.authorize(creds)
    except Exception:
        return None

# --- APP CONTENT ---
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
    notes = st.text_area("Notes")
    
    if st.form_submit_button("Submit to Lead Tracker"):
        if name and email:
            client = get_gspread_client()
            if client:
                try:
                    # Your Sheet ID
                    sheet = client.open_by_key("1V0emFdEceVa3JB5uctCw5PMYC-li_YvbZZFQmQwj0vI").sheet1
                    new_row = [name, email, phone, age, status, ", ".join(types), "N/A", m_pay, a_inc, notes]
                    sheet.append_row(new_row)
                    st.success("✅ Lead saved!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Sheet Error: {e}")
        else:
            st.warning("Please enter name and email.")
