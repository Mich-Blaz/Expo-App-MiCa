from sqlalchemy import create_engine, Column, Integer, String,Boolean, Float, DateTime,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Events(Base):
    __tablename__ = 'events'
    
    event_id = Column(Integer, primary_key=True)
    url = Column(Text, nullable=False)
    title = Column(Text, nullable=False)
    title_event = Column(Text)
    lead_text = Column(Text)
    description = Column(Text)
    address_name = Column(Text)
    locations = Column(JSONB)
    address_street = Column(Text)
    address_zipcode = Column(Text)
    address_city = Column(Text)
    address_text = Column(Text)
    lat_lon = Column(JSONB)
    date_start = Column(DateTime, default=datetime.now)
    date_end = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    has_card = Column(Boolean,default=0)
    access_link = Column(Text)
    access_link_text = Column(Text)
    address_url = Column(Text)
    address_url_text = Column(Text)
    address_name = Column(Text)
    qfap_tags = Column(Text)
    flag_interest = Column(Boolean)




    def __repr__(self):
        return f"<Events(event_id='{self.event_id}', title={self.title})>"

