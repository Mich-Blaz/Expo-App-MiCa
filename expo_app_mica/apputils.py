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
import pydeck as pdk

# Charger les variables d'environnement (optionnel en production)
load_dotenv()  # Ignoré si .env n'existe pas


# Créer l'engine
engine = create_engine(os.environ['DATABASE_URL'], echo=False,  pool_pre_ping=True, pool_size=5,    max_overflow=10)
Session = sessionmaker(bind=engine)
def apply_color(date_end,green=3,orange=8):
    now = datetime.now()
    if date_end < now + timedelta(weeks=green):
        return (205,30,0)
    elif date_end < now + timedelta(weeks=orange):
        return (255,153,51)
    else:
        return (124,252,0)
def transform_lat_lon(df):
    now = datetime.now()
    """Transforme la colonne lat_lon en deux colonnes lat et lon"""
    df['lat'] = df['lat_lon'].apply(lambda x: x['lat'])
    df['lon'] = df['lat_lon'].apply(lambda x: x['lon'])
    df['color'] = df['date_end'].apply(lambda x: apply_color(x))
    return df



def get_deck_maps(df):
          
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[lon, lat]',
            get_radius=100,
            get_fill_color='color', #tester get_color
            pickable=True,
        )

        view_state = pdk.ViewState(
            latitude=df["lat"].mean(),
            longitude=df["lon"].mean(),
            zoom=12,
        )

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": """
                <b>{title}</b><br/>
                Catégorie : {qfap_tags}
                """
            }
        )
        return deck

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

def check_password():
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == os.getenv("APP_PASSWORD"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    # Show input for password
    st.text_input(
        "Password", 
        type="password", 
        on_change=password_entered, 
        key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False