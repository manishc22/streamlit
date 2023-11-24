from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_stores import get_alerts, get_updated_store, get_image
from functions.get_store_data import get_store_data
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Store Digital Audits",
                   layout='wide', initial_sidebar_state='expanded')


final_store = ''

if 'refresh' not in st.session_state:
    st.session_state['refresh'] = 0

if 'counter' not in st.session_state:
    st.session_state['counter'] = 0

if 'img1_audited' not in st.session_state:
    st.session_state['img1_audited'] = False

if 'img2_audited' not in st.session_state:
    st.session_state['img2_audited'] = False


@st.cache_data
def get_data(count):
    df_images = get_store_data()
    return df_images


# df_images = get_data()
col100, col101 = st.columns([8, 1], gap='large')
with col101:
    with st.form(key="Refresh"):
        # st.write("Refresh")
        submit = st.form_submit_button("Refresh")
        if submit:
            st.session_state['refresh'] += 1
            df_refreshed = get_data(st.session_state['refresh'])
            st.session_state.counter = 0


if st.session_state['refresh'] == 0:
    df_alerts1 = pd.DataFrame()
else:
    df_alerts1 = get_data(st.session_state['refresh'])

if df_alerts1.shape[0] > 0:

    counter = st.session_state.counter

    def get_store_program(position_id, store):
        data = supabase.table('store_master').select(
            '"ProgramName"').eq('"SalesmanPositionId"', position_id).eq('"StoreName"', store).execute()
        return data.data

    st.write("### Audit App")
    tab1, tab2 = st.tabs(["Audits", "Reports"])

    # df_alerts1 = pd.DataFrame.from_records(get_store_data().data)

    total_images = df_alerts1.shape[0]

    with tab1:
        col1, col2, col3, col4 = st.columns([1, 2, 2, 2], gap='large')
        with col1:
            st.write(
                f"##### Image Number: {st.session_state.counter + 1} of {total_images}")

            df_alerts1['created_at'] = pd.to_datetime(
                df_alerts1['created_at']) + pd.Timedelta('05:30:00')
            print(df_alerts1['created_at'])
        id = df_alerts1.loc[counter, 'id'].item()
        position_id = df_alerts1.loc[counter, 'position_id']
        image = df_alerts1.loc[counter, 'image1_id']
        image2 = df_alerts1.loc[counter, 'image2_id']
        date = df_alerts1.loc[counter, 'created_at'].strftime('%d')
        month = df_alerts1.loc[counter, 'created_at'].strftime('%b')
        time = df_alerts1.loc[counter, 'created_at'].strftime('%X')

        store = df_alerts1.loc[counter, 'store_name']
        df_alerts1['img1_audited'] = False
        df_alerts1['img2_audited'] = False
        if int(date) <= 15:
            cycle = "Cycle1"
        else:
            cycle = "Cycle2"

        image_url = storage_url + image
        image2_url = storage_url + image2
        msg = "Date: " + date + " " + month + " " + \
            time + " |  " + cycle + " |  " + store
        with col2:
            st.write(f"##### PositionID - {position_id}")
            st.write(f"###### {msg}")

        with col3:
            store_name = get_alerts(position_id)

            if store_name.shape[0] > 0:
                select_store = store_name[store_name['StoreName'].str.startswith(
                    store[0])]
                updated_store = get_updated_store(id)
                if updated_store:
                    final_store = st.selectbox(updated_store,
                                               select_store)
                else:
                    final_store = st.selectbox(f"Similar Stores for {position_id}",
                                               select_store)

        def save_store():
            program = pd.DataFrame.from_records(
                get_store_program(position_id, final_store)).values[0][0]

            if program:
                data = supabase.table('store_audits').update(
                    {'store_name_updated': final_store}).eq('id', id).execute()
                data1 = supabase.table('store_audits').update(
                    {'program_name': program}).eq('id', id).execute()

        with col4:

            if final_store:
                st.button("Save Store", on_click=save_store)

        st.divider()

        def increment_counter():
            st.session_state.counter += 1

        def decrement_counter():
            st.session_state.counter -= 1

        col4, col5 = st.columns([2, 1], gap='large')
        st.divider()
        with col4:
            st.image(image_url)

        with col5:

            col10, col11, col12 = st.columns([1, 1, 1], gap='small')
            with col10:
                if counter >= 0:
                    st.button("Previous", on_click=decrement_counter)
            with col11:

                if counter < (total_images - 1):
                    st.button("Next Page", on_click=increment_counter)
            st.write(
                f"Dealerboard Image Submitted: {st.session_state['img1_audited']}")
            # st.write(
            #     f"Window Visibility Image Submitted: {st.session_state.img2_audited}")
            st.divider()
            with st.expander("Dealerboard Audit"):
                with st.form("Dealerboard Audit", clear_on_submit=True):
                    # image_correct = st.checkbox("Image Correct")
                    selfie = st.checkbox("Selfie with Dealerboard")
                    submitted = st.form_submit_button(
                        "Submit")
                    if submitted:

                        data_insert = supabase.table('dealerboard').insert(
                            {'form_id': id, 'selfie_dealerboard': selfie, 'month': month,
                                'cycle': cycle}).execute()

                        data = supabase.table('store_audits').update(
                            {'image1_audited': True}).eq('id', id).execute()

                        st.session_state['img1_audited'] = False

        col7, col8 = st.columns([2, 1], gap='large')

        with col7:
            st.image(image2_url)

        with col8:
            with st.expander("Window Visibility"):
                with st.form("Samrat Store Audit", clear_on_submit=True):

                    image_quality = st.checkbox("Image Quality")
                    num_window_kits = st.number_input(
                        'Number of Window Kits', min_value=0, max_value=10)
                    window_hotspot = st.checkbox("Window Hotspot")

                    st.divider()

                    p_window_exist = st.checkbox("Pediasure Window Exists")
                    p_eye_level = st.checkbox("Pediasure Eye Level")
                    p_backing_sheet = st.checkbox("Pediasure Backing Sheet")
                    p_four_shelf_strip = st.checkbox("Pediasure 4 Shelf Strip")
                    st.divider()

                    e_window_exist = st.checkbox("Ensure Window Exists")
                    e_eye_level = st.checkbox("Ensure Eye Level")
                    e_backing_sheet = st.checkbox("Ensure Backing Sheet")
                    e_four_shelf_strip = st.checkbox("Ensure 4 Shelf Strip")
                    st.divider()
                    all_brands = st.checkbox("All must win brands available")

                    submitted = st.form_submit_button(
                        "Submit")

                    if submitted:

                        data_insert = supabase.table('samrat').insert(
                            {'form_id': id, 'image_quality': image_quality, 'month': month, 'window_hotspot': window_hotspot,
                                'cycle': cycle, 'p_window_exist': p_window_exist, 'p_eye_level': p_eye_level, 'p_backing_sheet': p_backing_sheet, 'p_four_shelf_strip': p_four_shelf_strip, 'num_window_kits': num_window_kits, 'e_window_exist': e_window_exist, 'e_eye_level': e_eye_level, 'e_backing_sheet': e_backing_sheet, 'e_four_shelf_strip': e_four_shelf_strip, 'all_brands': all_brands}).execute()

                        data = supabase.table('store_audits').update(
                            {'image2_audited': True}).eq('id', id).execute()

                        df_alerts1.loc[counter, 'img2_audited'] = True
else:
    st.header("No data available")
