from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL = "sqlite:///./tasks.db"

engine = create_engine(URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()