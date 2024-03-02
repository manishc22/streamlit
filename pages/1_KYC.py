import random
from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_store_data import get_kyc_data, kyc_details_name, update_kyc

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_KYC_URL")

st.set_page_config(page_title="Store Digital Audits",
                   layout='wide', initial_sidebar_state='expanded')

if 'kyc_counter' not in st.session_state:
    st.session_state['kyc_counter'] = 0


forms = get_kyc_data()

def increment_counter():
            st.session_state.kyc_counter += 1

def decrement_counter():
    st.session_state.kyc_counter -= 1

regions = forms['RegionName'].drop_duplicates()
col1, col2, col3 = st.columns([1,2,1], gap='large')
kyc_counter = st.session_state.kyc_counter

def update_counter():
    st.session_state.kyc_counter = 0

with col1:
    region = st.selectbox('Regions', regions, on_change=update_counter)

forms_filter = forms[forms['RegionName']==region].reset_index()
total_images = forms_filter.shape[0]

with col3:
    col10, col11 = st.columns([1, 1], gap='small')
    
    with col10:
        if kyc_counter >= 0:
            st.button("Previous", on_click=decrement_counter)
    with col11:

        if kyc_counter < (total_images - 1):
            st.button("Next Page", on_click=increment_counter)
    
    
st.divider()    



col1, col2, col3, col4 = st.columns([1,2,1,2], gap='large')

id = forms_filter.loc[kyc_counter, 'id'].item()
position_id = forms_filter.loc[kyc_counter, 'position_id']
dealerboard = forms_filter.loc[kyc_counter, 'dealerboard']
aadhar = forms_filter.loc[kyc_counter, 'aadhar']
cheque = forms_filter.loc[kyc_counter, 'cheque']
date = forms_filter.loc[kyc_counter, 'created_at'].strftime('%d')
time = forms_filter.loc[kyc_counter, 'created_at'].strftime('%X')
gst = forms_filter.loc[kyc_counter,'gst']
gst_name = forms_filter.loc[kyc_counter,'gst_name']
store_name = forms_filter.loc[kyc_counter, 'store_name']
# print(type(id))
df_kyc_details = kyc_details_name(id)
print(df_kyc_details['beneficiary_name'][0])

if (dealerboard):
    dealerboard_url = storage_url + dealerboard
else:
    dealerboard_url = ''    
if (aadhar):
    aadhar_url = storage_url + aadhar
else:
    aadhar_url = ''    
cheque_url = storage_url + cheque


# def handlesubmit():
#     data = supabase.table('kyc_details').update(
#                             {'status': status}).eq('form_id', id).execute()

with col1:
    st.write(f"###### ID: {id}")
    st.write(
        f"###### Image: {st.session_state.kyc_counter + 1} of {total_images}")

    forms_filter['created_at'] = pd.to_datetime(
        forms_filter['created_at']) + pd.Timedelta('05:30:00')

with col2:
    st.write(f"###### PositionID - {position_id}")
    st.write(f"###### Store Name - {store_name}")


st.divider()    

col1, col2 = st.columns([2, 1])

with col1:
    if dealerboard_url:
        st.image(dealerboard_url)
with col2:
    st.write(f'###### GST: {gst}')
    st.write(f'###### GST Name: {gst_name}')        
    
st.divider()
col1, col2 = st.columns([2, 1])
with col1:
    st.image(cheque_url)

def text_to_array(string):
    return string[2:-2]

with col2:
    with st.form('Cheque Details'):
        name = st.text_input('Beneficiary Name', value = df_kyc_details['beneficiary_name'][0], key=1)
        acc = st.text_input('Account Number', value = df_kyc_details['account_no'][0], key=2)
        code = st.text_input('IFSC Code', value = df_kyc_details['bank_code'][0], key=3)
        aadhar_name = st.text_input('Aadhar Name', value = df_kyc_details['aadhar_name'][0], key=4)
        aadhar_no = st.text_input('Aadhar Name', value = df_kyc_details['aadhar_number'][0], key=5)
        status = st.selectbox('KYC Status', ('Pending', 'Success', 'Failed'), key=6)
        submitted = st.form_submit_button("Submit")
        if name:
            name = [text_to_array(name)]
        if acc:
            acc = [text_to_array(acc)]
        if code:
            code = [text_to_array(code)]
        if aadhar_name:
            aadhar_name = [text_to_array(aadhar_name)]
        if aadhar_no:
            aadhar_no = [text_to_array(aadhar_no)]

        print(acc, code, name)
        if submitted:
            update_kyc(id, code, name, acc, aadhar_no, aadhar_name, status)
            data = supabase.table('kyc_audits').update(
                            {'audited': True}).eq('id', id).execute()
st.divider()
col1, col2 = st.columns([2, 1])
with col1:
    if aadhar_url:
        st.image(aadhar_url)