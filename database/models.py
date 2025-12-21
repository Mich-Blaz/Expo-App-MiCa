from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    category = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price})>"



"""
id                  object
event_id             int64
url                 object
title               object
lead_text           object
description         object
date_start          object
date_end            object
locations           object
address_name        object
address_street      object
address_zipcode     object
address_city        object
lat_lon             object
access_link         object
access_link_text    object
updated_at          object
address_url         object
address_url_text    object
address_text        object
title_event         object
qfap_tags           object
"""