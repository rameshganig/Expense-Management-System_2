import streamlit as st
import sys
import os

# Change working directory to the Expense-Management-System_2 folder
# This ensures Streamlit finds .streamlit/secrets.toml in the correct location
app_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_dir)

# Add frontend to path
sys.path.insert(0, os.path.join(app_dir, 'frontend'))

from frontend.add_update_ui import add_update_tab
from frontend.analytics_ui import analytics_tab


st.set_page_config(
    page_title="Expense Tracking System",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 Expense Tracking System")

tab1, tab2 = st.tabs(["Add/Update", "Analytics"])

with tab1:
    add_update_tab()

with tab2:
    analytics_tab()
