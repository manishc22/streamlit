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

if 'yuvraj' not in st.session_state:

    st.session_state['yuvraj'] = 0

counter = st.session_state.yuvraj


def get_store_data():
    data = supabase.table('store_audits').select(
        'id', 'created_at', 'image2_id', 'store_name').eq('image2_audited', 'FALSE').eq('program_name', 'YUVRAJ').execute()
    return data


st.write("### Yuvraj Store Audits")
st.divider()

df_alerts1 = pd.DataFrame.from_records(get_store_data().data)

total_images = df_alerts1.shape[0]
col1, col2 = st.columns([1, 3], gap='large')
with col1:
    slider = st.slider("###### Total Images to be Audited",
                       counter, total_images, step=1)
    df_alerts1['created_at'] = pd.to_datetime(df_alerts1['created_at'])

st.divider()
id = df_alerts1.loc[counter, 'id']
image = (df_alerts1['image2_id']).values[counter]
date = df_alerts1.loc[counter, 'created_at'].strftime('%d')
month = df_alerts1.loc[counter, 'created_at'].strftime('%b')
time = df_alerts1.loc[counter, 'created_at'].strftime('%X')
store = df_alerts1.loc[counter, 'store_name']
if int(date) <= 15:
    cycle = "Cycle1"
else:
    cycle = "Cycle2"
image_id = image[10:46]
image_url = storage_url + image_id

msg = "Date: " + date + " " + month + " " + \
    time + " |  " + cycle + " |  "
with col2:
    st.write(f"###### {msg}")
    st.write(f"###### {store}")
col3, col4 = st.columns([2, 1], gap='large')
with col3:
    st.image(image_url, 400)


def increment_counter():
    st.session_state.yuvraj += 1


with col4:
    with st.form("Yuvraj Store Audit", clear_on_submit=True):
        image_correct = st.checkbox("Image Correct")
        image_quality = st.checkbox("Image Quality")
        window_exist = st.checkbox("Window Exists")
        eye_level = st.checkbox("Eye Level")
        backing_sheet = st.checkbox("Backing Sheet")
        four_shelf_strip = st.checkbox("4 Shelf Strip")
        num_window_kits = st.number_input(
            'Number of Window Kits', min_value=0, max_value=10)
        stock_quantity = st.number_input(
            'Stock Quantity', min_value=0, max_value=10)
        submitted = st.form_submit_button("Submit", on_click=increment_counter)
        if submitted:
            st.session_state.counter = st.session_state.counter + 1
            data_insert = supabase.table('yuvraj').insert(
                {'image_correct': image_correct, 'image_quality': image_quality, 'month': month,
                 'cycle': cycle, 'window_exist': window_exist, 'eye_level': eye_level, 'backing_sheet': backing_sheet, 'four_shelf_strip': four_shelf_strip, 'num_window_kits': num_window_kits, 'stock_quantity': stock_quantity}).execute()

            data, count = supabase.table('store_audits').update(
                {'image2_audited': True}).eq('id', id).execute()
