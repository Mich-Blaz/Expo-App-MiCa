import streamlit as st
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from expo_app_mica.apputils import get_all_events

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
        st.session_state['temporary_data'] = st.data_editor(st.session_state.data[st.session_state['cols_run']].sort_values(by='updated_at',ascending=False))
        id_simil = st.session_state['temporary_data'][['flag_interest','event_id']].sort_values(by='event_id') == st.session_state.data[['flag_interest','event_id']].sort_values(by='event_id')
        st.dataframe(st.session_state['data'].sort_values(by='event_id')[id_simil])


elif action == "See my interests":
    st.header("arrive sooooon")
    
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
