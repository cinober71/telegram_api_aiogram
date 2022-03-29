from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class SnOfPos(Base):
    __tablename__ = 'POS Serial Number'
    id = Column(Integer, primary_key=True)
    Model = Column(String(255))
    SN = Column(String(255))