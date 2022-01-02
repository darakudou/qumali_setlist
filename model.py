import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

engine = sqlalchemy.create_engine('sqlite:///db.sqlite3', echo=True)
Base = declarative_base()


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    documents = relationship("document")


class Document(Base):
    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('image.id'))
    charactor = Column(String)
    page = Column(Integer)
    block = Column(Integer)
    paragraph = Column(Integer)
    words = Column(String)
    symbol = Column(String)
    detected_break = Column(String)
    x = Column(Float)
    y = Column(Float)


Base.metadata.create_all(bind=engine)

