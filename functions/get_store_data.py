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
            """select * from store_audits 
               where image1_audited = FALSE or image2_audited = FALSE
               """)
        data = pd.read_sql_query(
            sql, conn)
    return data
