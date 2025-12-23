import sys
import os
import time
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from database.models import Base, Product

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

def wait_for_db(engine, max_retries=30):
    """Attend que PostgreSQL soit prêt"""
    for i in range(max_retries):
        try:
            engine.connect()
            print("✅ Connexion à PostgreSQL réussie!")
            return True
        except OperationalError:
            print(f"⏳ Attente de PostgreSQL... ({i+1}/{max_retries})")
            time.sleep(1)
    return False

def init_database():
    """Crée la base de données et ajoute des données d'exemple"""
    
    # Créer la connexion
    database_url = get_database_url()
    print(f"📡 Connexion à: {database_url.replace(os.getenv('POSTGRES_PASSWORD', ''), '***')}")
    
    engine = create_engine(database_url, echo=True)
    
    # Attendre que PostgreSQL soit prêt
    if not wait_for_db(engine):
        print("❌ Impossible de se connecter à PostgreSQL")
        return
    
    # Créer toutes les tables
    Base.metadata.create_all(engine)
    print("✅ Tables créées")
    
    # Créer une session
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Vérifier si des données existent déjà
    if session.query(Product).count() == 0:
        # Ajouter des données d'exemple
        sample_products = [
            Product(name="Laptop", price=999.99, category="Electronics"),
            Product(name="Souris", price=29.99, category="Electronics"),
            Product(name="Clavier", price=79.99, category="Electronics"),
            Product(name="Chaise de bureau", price=199.99, category="Furniture"),
            Product(name="Bureau", price=349.99, category="Furniture"),
        ]
        
        session.add_all(sample_products)
        session.commit()
        print(f"✅ {len(sample_products)} produits ajoutés à la base de données")
    else:
        print(f"ℹ️ La base contient déjà {session.query(Product).count()} produits")
    
    session.close()
    print("✅ Base de données initialisée avec succès!")

if __name__ == "__main__":
    init_database()