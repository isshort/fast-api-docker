from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String,unique=True)
    phone = Column(String)
    password=Column(String(255))
    age = Column(Integer)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())


class Album(Base):
    __tablename__ = "album"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User")


class News(Base):
    __tablename__ = "Document"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    Description = Column(String)
