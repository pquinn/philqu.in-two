from sqlalchemy import Column, Integer, String
from app.rewindr.database import Base

class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    artist = Column(String(256))

    def __init__(self, name=None, artist=None):
        self.name = name
        self.artist = artist

    def __repr__(self):
        return '<Album %r>' % (self.name)