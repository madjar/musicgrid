from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    DateTime
    )
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from zope.sqlalchemy import register
from .main import App


Base = declarative_base()
Session = scoped_session(sessionmaker())
register(Session)



class Root:
    pass


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    current_track_id = Column(Integer, ForeignKey('tracks.id'))

    current_track = relationship('Track')

    def __repr__(self):
        return '<User: %s>' % self.username


class Track(Base):
    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True)
    title = Column(Text)
    album = Column(Text)
    artist = Column(Text)
    cover = Column(Text)

    def __repr__(self):
        return '<Track: %s>' % self.title

    def to_dict(self):
        return {'album': self.album,
                'artist': self.artist,
                'title': self.title,
                'cover': self.cover}


class ListenedTrack(Base):
    __tablename__ = 'listening'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    track_id = Column(Integer, ForeignKey('tracks.id'), primary_key=True)
    time = Column(DateTime, primary_key=True)

    user = relationship(User, backref='past_tracks')
    track = relationship(Track)

    def __repr__(self):
        return '<ListenedTrack: user=%s title=%s time=%s>' % (self.user.username, self.track.title, self.time.isoformat())


def get_or_create(model, defaults=None, **kwargs):
    instance = Session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        params = dict((k, v) for k, v in kwargs.items())
        params.update(defaults or {})
        instance = model(**params)
        Session.add(instance)
        return instance, True
