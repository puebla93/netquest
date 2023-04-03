"""Module to add record model
"""

from sqlalchemy import Column, Integer, String, Text

from app.database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    img = Column(Text, index=True)
