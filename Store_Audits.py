from dotenv import load_dotenv
import pandas as pd
from supabase import create_client, Client
import os
import streamlit as st
from functions.get_stores import get_alerts, get_updated_store, get_samrat
from functions.get_store_data import get_store_data
load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)
storage_url = os.getenv("SUPABASE_STORAGE_URL")

st.set_page_config(page_title="Store Digital Audits",
                   layout='wide', initial_sidebar_state='expanded')


final_store = ''


if 'counter' not in st.session_state:
    st.session_state['counter'] = 0


df_alerts1 = get_store_data()

if df_alerts1.shape[0] > 0:

    counter = st.session_state.counter

    def get_store_program(position_id, store):
        data = supabase.table('abbott_master_jan').select(
            '"ProgramName"').eq('"SalesmanPositionID"', position_id).eq('"StoreName"', store).execute()
        return data.data

    st.write("### Audit App")
    tab1, tab2 = st.tabs(["Audits", "Reports"])

    # df_alerts1 = pd.DataFrame.from_records(get_store_data().data)

    total_images = df_alerts1.shape[0]
    id = df_alerts1.loc[counter, 'id'].item()
    with tab1:
        col1, col2, col3, col4 = st.columns([1, 2, 2, 2], gap='large')
        with col1:
            st.write(f"##### ID: {id}")
            st.write(
                f"##### Image Number: {st.session_state.counter + 1} of {total_images}")

            df_alerts1['created_at'] = pd.to_datetime(
                df_alerts1['created_at']) + pd.Timedelta('05:30:00')

        # id = df_alerts1.loc[counter, 'id'].item()
        position_id = df_alerts1.loc[counter, 'position_id']
        image = df_alerts1.loc[counter, 'image1_id']
        image2 = df_alerts1.loc[counter, 'image2_id']
        date = df_alerts1.loc[counter, 'created_at'].strftime('%d')
        month = df_alerts1.loc[counter, 'created_at'].strftime('%b')
        time = df_alerts1.loc[counter, 'created_at'].strftime('%X')
        program_name = df_alerts1.loc[counter, 'program_name']

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
            if program_name:
                st.write(f"###### Program Name: {program_name}")
            else:
                st.write(f"###### No program name available")
        with col3:
            store_name = get_alerts(position_id)
            # store_caps = store[0].capitalize()
        #     if store_name.shape[0] > 0:
        #         select_store = store_name[store_name['StoreName'].str.startswith(
        #             store_caps)]
        #         if select_store.shape[0] == 0:
        #             select_store = store_name[store_name['StoreName'].str.startswith(
        #                 store[0])]
        #         updated_store = get_updated_store(id)
        #         if updated_store:
        #             final_store = st.selectbox(updated_store,
        #                                        select_store)
        #         else:
        #             final_store = st.selectbox(f"Similar Stores for {position_id}",
        #                                        select_store)

        # def save_store():
        #     program = pd.DataFrame.from_records(
        #         get_store_program(position_id, final_store)).values[0][0]

        #     if program:
        #         data = supabase.table('store_audits').update(
        #             {'store_name_updated': final_store}).eq('id', id).execute()
        #         data1 = supabase.table('store_audits').update(
        #             {'program_name': program}).eq('id', id).execute()

        # with col4:

            # if final_store:
            #     st.button("Save Store", on_click=save_store)

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

            # dealerboard_rows = get_dealerboard(id)

            # if dealerboard_rows.shape[0] > 0:
            #     st.write(
            #         "Dealerboard Image Submitted: YES")
            # else:
            #     st.write(
            #         "Dealerboard Image Submitted: NO")

            samrat_rows = get_samrat(id)

            if samrat_rows.shape[0] > 0:
                st.write(
                    "AUDITED: YES")
            else:
                st.write(
                    "AUDITED: NO")
            st.divider()
            # with st.expander("Dealerboard Audit"):
            #     with st.form("Dealerboard Audit", clear_on_submit=False):
            #         # image_correct = st.checkbox("Image Correct")
            #         selfie = st.checkbox("Selfie with Dealerboard")
            #         submitted = st.form_submit_button(
            #             "Submit")
            #         if submitted:

            #             data_insert = supabase.table('dealerboard').insert(
            #                 {'form_id': id, 'selfie_dealerboard': selfie, 'month': month,
            #                     'cycle': cycle}).execute()

            #             data = supabase.table('store_audits').update(
            #                 {'image1_audited': True}).eq('id', id).execute()

        col7, col8 = st.columns([2, 1], gap='large')

        with col7:
            st.image(image2_url)

        with col8:
            with st.expander("Window Visibility"):
                with st.form("Samrat Store Audit", clear_on_submit=False):

                    selfie = st.checkbox("Selfie with Dealerboard")
                    num_window_kits = st.number_input(
                        'Number of Window Kits', min_value=0, max_value=10)

                    st.divider()

                    p_window_exist = st.checkbox("Pediasure Window Exists")
                    p_eye_level = st.checkbox("Pediasure Eye Level")
                    p_backing_sheet = st.checkbox("Pediasure Brand Block")

                    st.divider()

                    e_window_exist = st.checkbox("Ensure Window Exists")
                    e_eye_level = st.checkbox("Ensure Eye Level")
                    e_backing_sheet = st.checkbox("Ensure Brand Block")

                    st.divider()

                    s_window_exist = st.checkbox("Similac Window Exists")
                    s_eye_level = st.checkbox("Similac Eye Level")
                    s_backing_sheet = st.checkbox("Similac Brand Block")

                    st.divider()
                    all_brands = st.checkbox("All must win brands available")

                    submitted = st.form_submit_button(
                        "Submit")

                    if submitted:

                        data_insert = supabase.table('samrat').insert(
                            {'form_id': id, 'month': month,
                                'cycle': cycle, 'p_window_exist': p_window_exist, 'p_eye_level': p_eye_level, 'p_backing_sheet': p_backing_sheet, 'num_window_kits': num_window_kits, 'e_window_exist': e_window_exist, 'e_eye_level': e_eye_level, 'e_backing_sheet': e_backing_sheet, 's_window_exist': s_window_exist, 's_eye_level': s_eye_level, 's_backing_sheet': s_backing_sheet, 'all_brands': all_brands, 'selfie_dealerboard': selfie}).execute()

                        data = supabase.table('store_audits').update(
                            {'image1_audited': True}).eq('id', id).execute()


else:
    st.header("No data available")
