import pandas as pd
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def get_alerts(positionID):
    data = supabase.table('store_master').select(
        '"StoreName"').eq('"SalesmanPositionId"', positionID).execute()
    df_stores = pd.DataFrame.from_records(data.data)

    return df_stores


def get_updated_store(id):
    data = supabase.table('store_audits').select(
        'store_name_updated').eq('id', id).execute()
    store_name_updated = pd.DataFrame.from_records(
        data.data).loc[0, 'store_name_updated']

    return store_name_updated
