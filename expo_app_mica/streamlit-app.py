from asyncio import events
from sqlalchemy import create_engine
import streamlit as st
import sys
import os
from dotenv import load_dotenv
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_utils import update_events_interest_flag
from expo_app_mica.apputils import get_all_events,expose_selected_item
from apputils import transform_lat_lon,check_password,get_deck_maps,event_card

# Configuration de la page
st.set_page_config(
    page_title="Nos petites Expos !",
    page_icon="🥳",
    layout="wide"
)
load_dotenv()

if "cols_run" not in st.session_state:
    st.session_state['cols_run'] = ['flag_interest','event_id','title','date_start','date_end','address_name','qfap_tags','updated_at']

if "data" not in st.session_state or "categories" not in st.session_state:
    st.session_state['data'],st.session_state['categories'] = get_all_events()



# Do not continue if check_password is not True
if not check_password():
    st.stop()

st.title("Apps to manage your events list!")
st.markdown("---")

# Sidebar pour les actions
with st.sidebar:
    st.header("Actions")
    action = st.radio("Que voulez-vous faire ?", 
                      ["Select New Events !", "See my interests"])

# Affichage des produits
if action == "Select New Events !":
    st.header("List of Events !")
    
    
    if not st.session_state.data.empty:
        dummies = st.session_state.data.qfap_tags.str.get_dummies(sep=";")
        selected_categories = st.multiselect(
            "Filter by Categories/Tags:",
            options=st.session_state.categories,
            default='Expo'
        )
        if selected_categories:
            mask = dummies[selected_categories].any(axis=1)
            df_filtered = st.session_state.data[mask]
        else:
            df_filtered = st.session_state.data
        cols_to_remove = [col for col in st.session_state.cols_run if col !='flag_interest']
        df_edited = st.data_editor(
            df_filtered[st.session_state["cols_run"]]
                .sort_values(by="updated_at", ascending=False),
            key="editor",disabled=cols_to_remove,
        )        
        edited_rows = st.session_state["editor"]["edited_rows"]
        # st.write('edited_rows:', edited_rows)
        if edited_rows:
            changed = []
            for idx, changed_values in edited_rows.items():
                row = df_edited.iloc[idx].copy()
                for col, value in changed_values.items():
                    row[col] = value
                changed.append(row)

            df_changed = pd.DataFrame(changed)
            # st.dataframe(df_changed)
            l = [{'event_id': row['event_id'], 'flag_interest': row['flag_interest']} for _, row in df_changed.iterrows()]
            with st.form("update database with interest choices"):
                submitted = st.form_submit_button("Update database")
                if submitted:
                    event_ids_totrueflag = df_changed[df_changed['flag_interest']==True]['event_id'].tolist()
                    event_ids_to_falseflag = df_changed[df_changed['flag_interest']==False]['event_id'].tolist()
                    engine = create_engine(os.environ['DATABASE_URL'], echo=False,  pool_pre_ping=True, pool_size=5,    max_overflow=10)
                    update_events_interest_flag(event_ids_totrueflag,event_ids_to_falseflag,engine)
                    st.success("Database updated successfully!")
                    get_all_events.clear()
                    st.session_state['data'],st.session_state['categories'] = get_all_events()
            st.button('Reload pleaaase')

elif action == "See my interests":
    st.header("My interested Events !")
    df_interests = st.session_state.data[st.session_state.data['flag_interest']==True]
    if not df_interests.empty:  
 
        df_ints = transform_lat_lon(df_interests)
        deck = get_deck_maps(df_ints)
        st.pydeck_chart(deck,on_select="rerun",key='deck_interests')

        if 'deck_interests' in st.session_state:
            res = expose_selected_item(st.session_state['deck_interests'],df_ints)
            if res:
                # st.write("You selected:", res)
                event_card(res)
            else:
                st.info("Select a point on the map to see details here.")

    
st.markdown("---")
