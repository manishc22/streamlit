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

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

if 'samrat' not in st.session_state:
    st.session_state['samrat'] = 0

counter = st.session_state.samrat


def get_store_data():
    data = supabase.table('store_audits').select(
        'id', 'created_at', 'image2_id', 'store_name').eq('image2_audited', 'FALSE').eq('program_name', 'SAMRAT').execute()
    return data


st.write("### Samrat Store Audits")
st.divider()

df_alerts1 = pd.DataFrame.from_records(get_store_data().data)

total_images = df_alerts1.shape[0]
col1, col2 = st.columns([1, 3], gap='large')
with col1:
    st.write(f"##### Total Images: {total_images}")

    df_alerts1['created_at'] = pd.to_datetime(df_alerts1['created_at'])

st.divider()
id = df_alerts1.loc[counter, 'id']
image = df_alerts1.loc[counter, 'image2_id']
date = df_alerts1.loc[counter, 'created_at'].strftime('%d')
month = df_alerts1.loc[counter, 'created_at'].strftime('%b')
time = df_alerts1.loc[counter, 'created_at'].strftime('%X')
store = df_alerts1.loc[counter, 'store_name']
if int(date) <= 15:
    cycle = "Cycle1"
else:
    cycle = "Cycle2"
image_url = storage_url + image

msg = "Date: " + date + " " + month + " " + \
    time + " |  " + cycle + " |  " + store
with col2:
    st.write(f"##### {msg}")

col3, col4 = st.columns([2, 1], gap='large')
with col3:
    st.image(image_url, use_column_width='auto')


def increment_counter():
    st.session_state.samrat += 1


with col4:
    with st.form("Samrat Store Audit", clear_on_submit=True):
        image_correct = st.checkbox("Image Correct")
        image_quality = st.checkbox("Image Quality")
        p_window_exist = st.checkbox("PS Window Exists")
        p_eye_level = st.checkbox("PS Eye Level")
        p_backing_sheet = st.checkbox("PS Backing Sheet")
        p_four_shelf_strip = st.checkbox("PS 4 Shelf Strip")
        num_window_kits = st.number_input(
            'Number of Window Kits', min_value=0, max_value=10)
        p_stock_quantity = st.number_input(
            'PS Stock Quantity', min_value=0, max_value=10)
        window_hotspot = st.checkbox("Window Hotspot")
        e_window_exist = st.checkbox("Ensure Window Exists")
        e_eye_level = st.checkbox("Ensure Eye Level")
        e_backing_sheet = st.checkbox("Ensure Backing Sheet")
        e_four_shelf_strip = st.checkbox("Ensure 4 Shelf Strip")
        all_brands = st.checkbox("All must win brands available")

        p_7_stock_quantity = st.number_input(
            'PS 7+ Stock Quantity', min_value=0, max_value=10)
        e_stock_quantity = st.number_input(
            'Ensure Stock Quantity', min_value=0, max_value=10)
        ed_stock_quantity = st.number_input(
            'Ensure Diabetics Stock Quantity', min_value=0, max_value=10)
        submitted = st.form_submit_button("Submit", on_click=increment_counter)

        if submitted:
            st.session_state.counter = st.session_state.counter + 1
            data_insert = supabase.table('samrat').insert(
                {'image_correct': image_correct, 'image_quality': image_quality, 'month': month,
                 'cycle': cycle, 'p_window_exist': p_window_exist, 'p_eye_level': p_eye_level, 'p_backing_sheet': p_backing_sheet, 'p_four_shelf_strip': p_four_shelf_strip, 'num_window_kits': num_window_kits, 'p_stock_quantity': p_stock_quantity, 'e_window_exist': e_window_exist, 'e_eye_level': e_eye_level, 'e_backing_sheet': e_backing_sheet, 'e_four_shelf_strip': e_four_shelf_strip, 'e_stock_quantity': e_stock_quantity, 'ed_stock_quantity': ed_stock_quantity, 'p_7_stock_quantity': p_7_stock_quantity}).execute()

            data, count = supabase.table('store_audits').update(
                {'image2_audited': True}).eq('id', id).execute()
