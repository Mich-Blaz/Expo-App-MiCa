import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Events
import pandas as pd
import streamlit as st
# Charger les variables d'environnement (optionnel en production)
load_dotenv()  # Ignoré si .env n'existe pas


# Créer l'engine
engine = create_engine(os.environ['DATABASE_URL'], echo=False,  pool_pre_ping=True, pool_size=5,    max_overflow=10)
Session = sessionmaker(bind=engine)


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

