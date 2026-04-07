import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. Page Config
st.set_page_config(page_title="Insurance Lead Tracker", page_icon="🛡️")

# 2. Custom Color Styling (Teal Gradient + Pure Black Text)
st.markdown(
    """
    <style>
    /* 1. HIDER: Keeps the red bar and name invisible */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppToolbar {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    div[class^="viewerBadge"], div[class*="viewerBadge"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* 2. BACKGROUND: Using your chosen teal/grey-green colors */
    .stApp {
        background: linear-gradient(135deg, #49C6D6, #95C2C7);
        background-attachment: fixed;
    }

    /* 3. THE HIGHLIGHT KILLER: Targets the wrappers around labels */
    /* This removes the white background 'pill' from every text element */
    div[data-testid="stWidgetLabel"], 
    div[data-testid="stWidgetLabel"] div, 
    div[data-testid="stWidgetLabel"] p,
    .stMarkdown div, 
    .stMarkdown p {
        background-color: transparent !important;
        background: none !important;
        box-shadow: none !important;
    }

    /* 4. TEXT: Forces everything to Pure Black */
    .stMarkdown, label, p, .stAlert, .stSelectbox label, .stMultiSelect label {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 5. SINGLE LINE TITLE */
    .title-text {
        white-space: nowrap;
        font-size: 2.1rem !important;
        font-weight: 700;
        color: #000000;
        text-align: center;
        padding: 10px 0px;
        margin-top: -40px;
    }

    /* 6. INPUT BOX CORNERS (Optional: makes them look sharper) */
    .stTextInput div, .stNumberInput div, .stSelectbox div, .stMultiSelect div {
        border-radius: 8px !important;
    }
    </style>
    <h1 class="title-text">🛡️ Personal Risk Protection Analyzer</h1>
    """,
    unsafe_allow_html=True
)

   /* 3. TEXT: This forces the text containers to be transparent */
    .stMarkdown, label, p, .stAlert, .stSelectbox label, .stMultiSelect label, div[data-testid="stExpander"] p {
        color: #000000 !important;
        background-color: transparent !important;
        background: none !important;
    }

    /* THE FIX: Specifically targets the 'pill' background around labels */
    div[data-testid="stWidgetLabel"] div, 
    div[data-testid="stWidgetLabel"] p,
    .st-emotion-cache-16idsys p {
        background-color: transparent !important;
        background: transparent !important;
        box-shadow: none !important;
        border: none !important;
    }

    /* Ensures the text itself doesn't have a highlight shadow */
    span {
        background-color: transparent !important;
    }

    /* This targets the specific wrapper Streamlit uses for Form Labels */
    div[data-testid="stWidgetLabel"] p {
        background-color: transparent !important;
        color: #000000 !important;
    }
    /* 4. TITLE: One line, Black, positioned at the top */
    .title-text {
        white-space: nowrap;
        font-size: 2.1rem !important;
        font-weight: 700;
        color: #000000;
        text-align: center;
        padding: 10px 0px;
        margin-top: -40px;
    }

    /* 5. FORM BOXES: Optional - making input boxes slightly transparent 
       to look better with the teal background */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stMultiSelect div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: black !important;
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
    except Exception as e:
        return None

# --- APP CONTENT ---
# (Note: I removed the st.title() line from here to prevent the double title)

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
                    sheet = client.open_by_key("1V0emFdEceVa3JB5uctCw5PMYC-li_YvbZZFQmQwj0vI").sheet1
                    new_row = [name, email, phone, age, status, ", ".join(types), "N/A", m_pay, a_inc, notes]
                    sheet.append_row(new_row)
                    st.success("✅ Lead saved! Aman will contact you shortly.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Sheet Error: {e}")
        else:
            st.warning("Please enter name and email.")
