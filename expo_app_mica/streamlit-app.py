from sqlalchemy import create_engine
import streamlit as st
import sys
import os
from dotenv import load_dotenv
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_utils import update_events_interest_flag
from expo_app_mica.apputils import get_all_events
from apputils import transform_lat_lon,check_password,get_deck_maps

# Configuration de la page
st.set_page_config(
    page_title="Nos petites Expos !",
    page_icon="🥳",
    layout="wide"
)
load_dotenv()

if "cols_run" not in st.session_state:
    st.session_state['cols_run'] = ['flag_interest','event_id','title','date_start','date_end','address_name','qfap_tags','updated_at']

if "data" not in st.session_state:
    st.session_state['data'] = get_all_events()



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
        df_edited = st.data_editor(
            st.session_state.data[st.session_state["cols_run"]]
                .sort_values(by="updated_at", ascending=False),
            key="editor"
        )        
        edited_rows = st.session_state["editor"]["edited_rows"]
        st.write('edited_rows:', edited_rows)
        if edited_rows:
            changed = []
            for idx, changed_values in edited_rows.items():
                row = df_edited.iloc[idx].copy()
                for col, value in changed_values.items():
                    row[col] = value
                changed.append(row)

            df_changed = pd.DataFrame(changed)
            st.dataframe(df_changed)
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
                    st.session_state['data'] = get_all_events()
            st.button('Reload pleaaase')

elif action == "See my interests":
    st.header("My interested Events !")
    df_interests = st.session_state.data[st.session_state.data['flag_interest']==True]
    if not df_interests.empty:  
        st.dataframe(
            df_interests#[st.session_state["cols_run"]]
                .sort_values(by="updated_at", ascending=False),
            use_container_width=True
        )
        df_ints = transform_lat_lon(df_interests)
        # st.write(df_ints)
        deck = get_deck_maps(df_ints)
        st.pydeck_chart(deck)

    
    # with st.form("add_product_form"):
    #     name = st.text_input("Nom du produit")
    #     price = st.number_input("Prix (€)", min_value=0.0, step=0.01)
    #     category = st.selectbox("Catégorie", ["Electronics", "Furniture", "Clothing", "Food", "Other"])
        
    #     submitted = st.form_submit_button("Ajouter")
        
    #     if submitted:
    #         if name and price > 0:
    #             if add_product(name, price, category):
    #                 st.success(f"✅ Produit '{name}' ajouté avec succès!")
    #                 st.balloons()
    #             else:
    #                 st.error("❌ Erreur lors de l'ajout du produit")
    #         else:
    #             st.warning("⚠️ Veuillez remplir tous les champs correctement")

# Supprimer un produit
# elif action == "Supprimer un produit":
#     st.header("Supprimer un produit")
    
#     df = get_products_df()
    
#     if not df.empty:
#         product_id = st.selectbox(
#             "Sélectionnez un produit à supprimer",
#             options=df['ID'].tolist(),
#             format_func=lambda x: f"{df[df['ID']==x]['Nom'].values[0]} (ID: {x})"
#         )
        
#         if st.button("🗑️ Supprimer", type="primary"):
#             if delete_product(product_id):
#                 st.success("✅ Produit supprimé avec succès!")
#                 st.rerun()
#             else:
#                 st.error("❌ Erreur lors de la suppression")
#     else:
#         st.info("Aucun produit à supprimer")

# Footer
st.markdown("---")
