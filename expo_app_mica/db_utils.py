import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Product
import pandas as pd

# Charger les variables d'environnement (optionnel en production)
load_dotenv()  # Ignoré si .env n'existe pas

def get_database_url():
    """Construit l'URL de connexion PostgreSQL"""
    user = os.getenv('POSTGRES_USER', 'myuser')
    password = os.getenv('POSTGRES_PASSWORD', 'mypassword')
    host = os.getenv('POSTGRES_HOST', 'localhost')
    port = os.getenv('POSTGRES_PORT', '5432')
    db = os.getenv('POSTGRES_DB', 'mydb')
    
    return f'postgresql://{user}:{password}@{host}:{port}/{db}'

# Créer l'engine
engine = create_engine(get_database_url())
Session = sessionmaker(bind=engine)

def get_all_products():
    """Récupère tous les produits"""
    session = Session()
    try:
        products = session.query(Product).all()
        return products
    finally:
        session.close()

def get_products_df():
    """Récupère les produits sous forme de DataFrame"""
    session = Session()
    try:
        products = session.query(Product).all()
        data = [{
            'ID': p.id,
            'Nom': p.name,
            'Prix': p.price,
            'Catégorie': p.category,
            'Créé le': p.created_at
        } for p in products]
        return pd.DataFrame(data)
    finally:
        session.close()

def add_product(name, price, category):
    """Ajoute un nouveau produit"""
    session = Session()
    try:
        new_product = Product(name=name, price=price, category=category)
        session.add(new_product)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"Erreur: {e}")
        return False
    finally:
        session.close()

def delete_product(product_id):
    """Supprime un produit par son ID"""
    session = Session()
    try:
        product = session.query(Product).filter(Product.id == product_id).first()
        if product:
            session.delete(product)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Erreur: {e}")
        return False
    finally:
        session.close()