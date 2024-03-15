import random
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_store_data import duplicate_rows

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_KYC_URL")

st.set_page_config(page_title="Store Digital Audits",
                   layout='wide', initial_sidebar_state='expanded')

if 'kyc_counter' not in st.session_state:
    st.session_state['kyc_counter'] = 0

df_duplicate = duplicate_rows()
total_rows = df_duplicate.shape[0]


col1, col2, col3 = st.columns([1,1,2], gap='large')
kyc_counter = st.session_state.kyc_counter


def update_counter():
    st.session_state.kyc_counter = 0


def increment_counter():
            st.session_state.kyc_counter += 1

def decrement_counter():
    st.session_state.kyc_counter -= 1


with col3:
    
    col10, col11 = st.columns([1, 1], gap='small')
    
    with col10:
        if kyc_counter < 0:
            update_counter()
        if kyc_counter > 0:
            st.button("Previous", on_click=decrement_counter)
    with col11:

        if kyc_counter < (total_rows - 1):
            st.button("Next Page", on_click=increment_counter)
    
    
st.divider()    

col1, col2, col3, col4 = st.columns([1,2,2,1], gap='large')

id = df_duplicate.loc[kyc_counter, 'id'].item()
position_id = df_duplicate.loc[kyc_counter, 'position_id'][0]

if (df_duplicate.loc[kyc_counter, 'aadhar_name'] != None):
    aadhar = df_duplicate.loc[kyc_counter, 'aadhar_name'][0]
    

cheque = df_duplicate.loc[kyc_counter, 'cheque']

if (df_duplicate.loc[kyc_counter, 'gst_name'] != None):
    gst_name = df_duplicate.loc[kyc_counter,'gst_name']

store_name = df_duplicate.loc[kyc_counter, 'store_name'][0]
status = df_duplicate.loc[kyc_counter, 'status']
print(status)
cheque_url = storage_url + cheque

with col1:
    st.write(f"###### ID: {id}")
    st.write(
        f"###### Image: {st.session_state.kyc_counter + 1} of {total_rows}")

    
with col2:
    st.write(f"###### PositionID - {position_id}")
    st.write(f"###### Store Name - {store_name}")

with col3:
    st.write(f"##### Status: {status}")
st.divider()    

col1, col2 = st.columns([2, 1])

with col1:
    
    st.write(f'###### GST Name: {gst_name}')     
    st.write(f'###### Aadhar Name: {aadhar}')   
    
st.divider()
col1, col2 = st.columns([2, 1])
with col1:
    st.image(cheque_url)
