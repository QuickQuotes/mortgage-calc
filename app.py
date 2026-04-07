import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. Page Config
st.set_page_config(page_title="Insurance Lead Tracker", page_icon="🛡️")

# 2. THE SUPER-HIDER STYLING
st.markdown(
    """
    <style>
    /* HIDES MAIN MENU AND FOOTER */
    #MainMenu, footer, header {visibility: hidden !important;}
    .stAppToolbar {display: none !important;}

    /* PUSHES THE USERNAME BADGE OFF THE ENTIRE UNIVERSE */
    [data-testid="stStatusWidget"],
    .st-emotion-cache-1vt458s,
    .st-emotion-cache-kg9bc0,
    .st-emotion-cache-1wbqy7s,
    div[class*="viewerBadge"],
    a[href*="aamanchand1-afk"] {
        position: fixed !important;
        left: -10000vw !important;
        bottom: -10000vh !important;
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
    }

    /* BACKGROUND COLOR & TEXT FIXES */
    .stApp {
        background: linear-gradient(135deg, #49C6D6, #95C2C7);
        background-attachment: fixed;
    }

    div[data-testid="stWidgetLabel"] p, label, p, span {
        background-color: transparent !important;
        color: #000000 !important;
    }

    .title-text {
        font-size: 2.1rem !important;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-top: -40px;
    }
    </style>
    <h1 class="title-text">🛡️ Personal Risk Protection Analyzer</h1>
    """,
    unsafe_allow_html=True
)

# 3. GOOGLE SHEETS LOGIC
def get_gspread_client():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        info = dict(st.secrets["gcp_service_account"])
        info["private_key"] = info["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(info, scopes=scope)
        return gspread.authorize(creds)
    except Exception:
        return None

# 4. APP CONTENT
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
        st.success("✅ Lead saved!")
