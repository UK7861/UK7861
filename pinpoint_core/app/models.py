from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

SQLALCHEMY_DATABASE_URL = "sqlite:///./pinpoint.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String) # Stored in plain text as per requirements
    business_number = Column(String)
    industry_type = Column(String)

    branches = relationship("Branch", back_populates="owner")

class Branch(Base):
    __tablename__ = "branches"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))
    branch_name = Column(String, index=True)
    business_address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    owner = relationship("Tenant", back_populates="branches")

def init_db():
    Base.metadata.create_all(bind=engine)
