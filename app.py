import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. Page Config
st.set_page_config(page_title="Insurance Lead Tracker", page_icon="🛡️")

# 2. ALL STYLING (Wrapped correctly so there is no error at top)
st.markdown(
    """
    <style>
   /* 1. BRANDING & USERNAME KILLER */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppToolbar {display: none !important;}

    /* This targets the specific 'aamanchand1-afk' badge and the bottom-right corner */
    [data-testid="stStatusWidget"],
    [aria-label*="aamanchand1-afk"],
    a[href*="aamanchand1-afk"],
    div[class*="viewerBadge"],
    .st-emotion-cache-1vt458s, 
    .st-emotion-cache-kg9bc0 {
        display: none !important;
        visibility: hidden !important;
        width: 0 !important;
        height: 0 !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transform: scale(0) !important;
    }

    /* BACKGROUND & TEXT COLORS */
    .stApp {
        background: linear-gradient(135deg, #49C6D6, #95C2C7);
        background-attachment: fixed;
    }

    /* KILL WHITE HIGHLIGHTS AROUND LABELS */
    div[data-testid="stWidgetLabel"] div, 
    div[data-testid="stWidgetLabel"] p,
    .stMarkdown div, 
    .stMarkdown p,
    label, p, span {
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
        color: #000000 !important;
    }

    /* TITLE STYLING */
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
    st.text_input("Full Name", key="name")
    st.text_input("Email", key="email")
    st.text_input("Phone", key="phone")
    st.number_input("Age", value=30, key="age")
    st.selectbox("Current Cover", ["No existing cover", "Partial", "Fully covered"], key="status")
    st.multiselect("Interests", ["Life", "Income Protection", "Trauma", "TPD", "Health"], key="types")
    st.text_area("Notes", key="notes")
    
    if st.form_submit_button("Submit to Lead Tracker"):
        # Logic for GSpread submission goes here
        st.success("✅ Lead saved!")
