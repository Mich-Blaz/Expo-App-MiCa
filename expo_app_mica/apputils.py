import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime,timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Events
from database.db_utils import update_events_interest_flag
import pandas as pd
import streamlit as st
# Charger les variables d'environnement (optionnel en production)
load_dotenv()  # Ignoré si .env n'existe pas


# Créer l'engine
engine = create_engine(os.environ['DATABASE_URL'], echo=False,  pool_pre_ping=True, pool_size=5,    max_overflow=10)
Session = sessionmaker(bind=engine)
def apply_color(date_end,green=3,orange=8):
    now = datetime.now()
    if date_end < now + timedelta(weeks=green):
        return (255,69,0)
    elif date_end < now + timedelta(weeks=orange):
        return (100,65,0)
    else:
        return (124,252,0)
def transform_lat_lon(df):
    now = datetime.now()
    """Transforme la colonne lat_lon en deux colonnes lat et lon"""
    df['lat'] = df['lat_lon'].apply(lambda x: x['lat'])
    df['lon'] = df['lat_lon'].apply(lambda x: x['lon'])
    df['color'] = df['date_end'].apply(lambda x: apply_color(x))
    return df



@st.cache_data
def get_all_events():
    """Récupère tous les events"""
    session = Session()
    try:
        events = session.query(Events).all()
        events = [k.__dict__ for k in events]
        df = pd.DataFrame(events).drop('_sa_instance_state',axis=1)
        return df

    finally:
        session.close()

