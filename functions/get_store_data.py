import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text, URL
import psycopg2


load_dotenv()


def sql_engine():
    engine = create_engine(
        "postgresql://postgres.menngmczcnnppczwxokk:z8sbaqh10domUZS3@aws-0-us-east-1.pooler.supabase.com:6543/postgres")
    return engine


@st.cache_data(ttl=3600)
def get_store_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from audit_status
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data


@st.cache_data(ttl=1800)
def get_kyc_data():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from kyc_audits where audited = 'FALSE'
               """)
        data = pd.read_sql_query(
            sql, conn)
        conn.close()
    return data

@st.cache_data(ttl=7200)
def kyc_details_name(id):
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(
            """select * from kyc_details where form_id = :id
               """)
        data = pd.read_sql_query(
            sql, conn, params={'id': int(id)})
        conn.close()
    return data

def update_kyc(form_id, code, name, account, aadhar_no, aadhar_name, status, failure_reason):
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text(""" update kyc_details 
        set account_no = :account, beneficiary_name = :name, bank_code = :code, aadhar_name = :aadhar_name, aadhar_number = :aadhar_no, status = :status, failure_reason = :failure_reason
                   where form_id = :form_id""")            
        conn.execute(sql, {"form_id":int(form_id), 'code':code, 'name':name, 'account':account, 'aadhar_name':aadhar_name, 'aadhar_no': aadhar_no, 'status':status, 'failure_reason': failure_reason})
    conn.close()    
    return None


def get_current_status (form_id):
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text("""select status from kyc_details where form_id = :form_id
               """)            
        data = pd.read_sql_query(
            sql, conn, params={'form_id': form_id})
        conn.close()  
    return data

@st.cache_data(ttl=3600)
def duplicate_rows():
    engine = sql_engine()
    with engine.begin() as conn:
        sql = text("""
                with count as (
                select store_name, position_id, count(store_name) as count_stores
                from kyc_current_status
                group by store_name, position_id),
                data as (
                select * from count where count_stores > 2)
                select * from kyc_current_status a, data where a.store_name = data.store_name and a.position_id = data.position_id
                order by a.position_id, a.store_name
                """)
        data = pd.read_sql_query(sql, conn)
        conn.close()
        return data
