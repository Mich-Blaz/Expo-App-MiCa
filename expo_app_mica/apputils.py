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
    df = df.copy()
    now = datetime.now()
    """Transforme la colonne lat_lon en deux colonnes lat et lon"""
    df['lat'] = df['lat_lon'].apply(lambda x: x['lat'])
    df['lon'] = df['lat_lon'].apply(lambda x: x['lon'])
    df.loc[:,'color'] = df['date_end'].apply(lambda x: apply_color(x))
    return df


def get_deck_maps(df):
        
    point_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        id="selected-point-layer",
        get_position=["lon", "lat"],
        get_color="color",
        pickable=True,
        auto_highlight=True,
        get_radius=100,
    )

    view_state = pdk.ViewState(
            latitude=df["lat"].mean(),
            longitude=df["lon"].mean(),
            zoom=12,
        )
    tooltip={
                "html": """
                <b>{title}</b><br/>
                Catégorie : {qfap_tags}
                """ }

    chart = pdk.Deck(
        point_layer,
        initial_view_state=view_state,
        tooltip=tooltip,
        )
    return chart

@st.cache_data
def get_all_events():
    """Récupère tous les events"""
    session = Session()
    try:
        events = session.query(Events).all()
        events = [k.__dict__ for k in events]
        df = pd.DataFrame(events).drop('_sa_instance_state',axis=1)
        df["categorie_list"] = df["qfap_tags"].fillna('Unknown').str.split(";")

        return df,sorted(
    {cat for sublist in df["categorie_list"] for cat in sublist}
)

    finally:
        session.close()

def expose_selected_item(item,df):
    if 'selected-point-layer' in item.selection.objects.keys():
        evid = item.selection.objects['selected-point-layer'][0]['event_id']
        selec = df[df['event_id']==evid].astype(str).to_dict(orient='records')[0]   
        return selec
    else: 
        return None
    
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

def is_valid(value):
    if value is None:
        return False
    if isinstance(value, str) and value.strip().lower() in {"none", ""}:
        return False
    return True
import streamlit as st

def event_card(event: dict):
    with st.container(border=True):

        # ─── TITRE ──────────────────────────────────────────
        if is_valid(event.get("title")):
            st.markdown(f"## {event['title']}")

        if is_valid(event.get("lead_text")):
            st.caption(event["lead_text"])

        # ─── DATES ──────────────────────────────────────────
        if is_valid(event.get("date_start")) or is_valid(event.get("date_end")):
            cols = st.columns(2)
            if is_valid(event.get("date_start")):
                cols[0].markdown(f"**📅 Début**  \n{event['date_start']}")
            if is_valid(event.get("date_end")):
                cols[1].markdown(f"**⏱️ Fin**  \n{event['date_end']}")

        # ─── LIEU ───────────────────────────────────────────
        location_fields = [
            event.get("address_name"),
            event.get("address_street"),
            event.get("address_zipcode"),
            event.get("address_city")
        ]

        if any(is_valid(v) for v in location_fields):
            st.markdown("### 📍 Lieu")

            if is_valid(event.get("address_name")):
                st.markdown(f"**{event['address_name']}**")

            address_line = " ".join(
                filter(
                    is_valid,
                    [
                        event.get("address_street"),
                        event.get("address_zipcode"),
                        event.get("address_city"),
                    ],
                )
            )
            if address_line:
                st.markdown(address_line)

        # ─── DESCRIPTION ────────────────────────────────────
        if is_valid(event.get("description")):
            st.markdown("### 🖼️ Description")
            st.markdown(event["description"], unsafe_allow_html=True)

        # ─── TAGS / META ────────────────────────────────────
        meta_cols = st.columns(2)

        if is_valid(event.get("qfap_tags")):
            meta_cols[0].markdown(f"**Type**  \n{event['qfap_tags']}")

        if is_valid(event.get("flag_interest")):
            meta_cols[1].markdown(
                "**À la une**  \nOui" if event["flag_interest"] == "True" else ""
            )

        # ─── LIENS ──────────────────────────────────────────
        if is_valid(event.get("url")) or is_valid(event.get("access_link")):
            st.markdown("### 🔗 Liens")

            if is_valid(event.get("url")):
                st.link_button("Page événement", event["url"])

            if is_valid(event.get("access_link")):
                st.link_button(
                    event.get("access_link_text", "Plus d'infos"),
                    event["access_link"],
                )
    