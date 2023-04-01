from sqlalchemy import Column, Integer, String, Text

from database import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    img = Column(Text, index=True)
