from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Audit Reports",
                   layout='wide', initial_sidebar_state='expanded')

tab1, tab2, tab3 = st.tabs(["Dashboard", "Dealerboard", "Window Visibility"])
with tab1:
    st.header("Dashboard")

with tab2:
    st.header("Dealerboard Reporting")

with tab3:
    st.header("Window Visibility Reporting")
