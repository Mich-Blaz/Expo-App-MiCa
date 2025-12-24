import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from expo_app_mica.db_utils import get_products_df, add_product, delete_product

# Configuration de la page
st.set_page_config(
    page_title="Gestion de Produits",
    page_icon="📦",
    layout="wide"
)
load_dotenv()

def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == os.getenv("APP_PASSWORD"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated
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

st.title("📦 Application de Gestion de Produits")
st.markdown("---")

# Sidebar pour les actions
with st.sidebar:
    st.header("Actions")
    action = st.radio("Que voulez-vous faire ?", 
                      ["Voir les produits", "Ajouter un produit", "Supprimer un produit"])

# Affichage des produits
if action == "Voir les produits":
    st.header("Liste des Produits")
    
    df = get_products_df()
    
    if not df.empty:
        # Statistiques
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Nombre de produits", len(df))
        with col2:
            st.metric("Prix moyen", f"{df['Prix'].mean():.2f} €")
        with col3:
            st.metric("Prix total", f"{df['Prix'].sum():.2f} €")
        
        st.markdown("---")
        
        # Tableau de données
        st.dataframe(df, use_container_width=True)
        
        # Graphique
        st.subheader("Prix par catégorie")
        category_prices = df.groupby('Catégorie')['Prix'].sum()
        st.bar_chart(category_prices)
    else:
        st.warning("Aucun produit dans la base de données")

# Ajouter un produit
elif action == "Ajouter un produit":
    st.header("Ajouter un nouveau produit")
    
    with st.form("add_product_form"):
        name = st.text_input("Nom du produit")
        price = st.number_input("Prix (€)", min_value=0.0, step=0.01)
        category = st.selectbox("Catégorie", ["Electronics", "Furniture", "Clothing", "Food", "Other"])
        
        submitted = st.form_submit_button("Ajouter")
        
        if submitted:
            if name and price > 0:
                if add_product(name, price, category):
                    st.success(f"✅ Produit '{name}' ajouté avec succès!")
                    st.balloons()
                else:
                    st.error("❌ Erreur lors de l'ajout du produit")
            else:
                st.warning("⚠️ Veuillez remplir tous les champs correctement")

# Supprimer un produit
elif action == "Supprimer un produit":
    st.header("Supprimer un produit")
    
    df = get_products_df()
    
    if not df.empty:
        product_id = st.selectbox(
            "Sélectionnez un produit à supprimer",
            options=df['ID'].tolist(),
            format_func=lambda x: f"{df[df['ID']==x]['Nom'].values[0]} (ID: {x})"
        )
        
        if st.button("🗑️ Supprimer", type="primary"):
            if delete_product(product_id):
                st.success("✅ Produit supprimé avec succès!")
                st.rerun()
            else:
                st.error("❌ Erreur lors de la suppression")
    else:
        st.info("Aucun produit à supprimer")

# Footer
st.markdown("---")
st.markdown("*Application Streamlit + PostgreSQL + Docker*")