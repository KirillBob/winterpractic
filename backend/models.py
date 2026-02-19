from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from .db import Base


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    extension = Column(String(64), nullable=True)
    size = Column(Integer)
    path = Column(String(1024), unique=True, index=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    comment = Column(String(1024))
