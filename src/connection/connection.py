import os
from unittest.mock import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

"""
Arquivo de configuração da conexão com o banco de dados usando SQLAlchemy
"""

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()