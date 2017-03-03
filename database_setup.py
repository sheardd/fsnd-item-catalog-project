from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)

class Artist(Base):
    __tablename__ = 'artist'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    image = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_rel = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'image'        : self.image,
       }
 
class Album(Base):
    __tablename__ = 'album'

    name =Column(String(250), nullable = False)
    id = Column(Integer, primary_key = True)
    artist =Column(String(250), nullable = False)
    year = Column(String(4))
    genre = Column(String(80))
    artwork = Column(String(250))
    artist_id = Column(Integer,ForeignKey('artist.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    artist_rel = relationship(Artist)
    user_rel = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'artist'         : self.artist,
           'id'         : self.id,
           'year'         : self.year,
           'genre'         : self.genre,
           'artwork'         : self.artwork,
       }

class Track(Base):
    __tablename__ = 'track'

    name =Column(String(250), nullable = False)
    id = Column(Integer, primary_key = True)
    artist =Column(String(250), nullable = False)
    album =Column(String(250), nullable = False)
    num = Column(Integer)
    artist_id = Column(Integer,ForeignKey('artist.id'),nullable=False)
    album_id = Column(Integer,ForeignKey('album.id'),nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'),nullable=False)
    artist_rel = relationship(Artist)
    album_rel = relationship(Artist)
    user_rel = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'artist'         : self.artist,
           'album'         : self.album,
           'id'         : self.id,
           'num'        : self.num,
       }


engine = create_engine('postgresql+psycopg2://catalog:udacity@localhost/mitunes')
 

Base.metadata.create_all(engine)
