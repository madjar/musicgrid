import datetime
from collections import Counter

from sqlalchemy.sql import func
from sqlalchemy import desc

from .main import App
from .model import *
from .collection import *


@App.json(model=Root)
def root(self, request):
    tracks = Counter(user.current_track for user in Session.query(User) if user.current_track)
    now_playing = [{'track': t.to_dict(),
                    'count': c} for (t, c) in tracks.items()]
    return {'now_playing': now_playing}


@App.json(model=Root, name='top')
def top(self, request):
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    track_ids_count = (Session.query(ListenedTrack.track_id, func.count('*')
                                     .label('listened'))
                       .filter(ListenedTrack.time > one_week_ago)
                       .group_by(ListenedTrack.track_id)
                       .order_by(desc('listened'))
                       .limit(50))
    top_tracks = [{'track': Session.query(Track).get(track_id).to_dict(),
                   'count': count}
                  for (track_id, count) in track_ids_count]
    return {'top_tracks': top_tracks}


@App.json(model=UserCollection, request_method='GET')
def users(self, request):
    return {'users': [user.username for user in self.query()]}


@App.json(model=UserCollection, request_method='POST')
def add_user(self, request):
    get_or_create(User, username=request.json['username'])
    return {'users': [user.username for user in self.query()]}
