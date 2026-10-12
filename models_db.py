from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry
import datetime

# PostgreSQL Database Connection URL (Update with your credentials)
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/ethiosoil_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FarmAdvisoryLog(Base):
    __tablename__ = "farm_advisory_logs"

    id = Column(Integer, primary_key=True, index=True)
    kebele_name = Column(String, index=True)
    farm_size_hectares = Column(Float)
    
    # PostGIS spatial point for latitude and longitude (SRID 4326 is standard WGS84 GPS)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)
    
    soil_ph = Column(Float)
    nitrogen_n = Column(Float)
    phosphorus_p = Column(Float)
    potassium_k = Column(Float)
    rainfall = Column(Float)
    
    recommended_crop = Column(String)
    acidity_status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    """Creates tables in PostgreSQL and enables PostGIS if not already active."""
    # Ensure PostGIS extension is created first in your postgres shell: CREATE EXTENSION postgis;
    Base.metadata.create_all(bind=engine)