import datetime

import transaction
import pylast
import spotipy

from .model import *
from .main import create_db


def get_cover_from_spotify(track, artist):
    spotify = spotipy.Spotify()

    query = 'track:"%s" artist:"%s"' % (track, artist)
    results = spotify.search(q=query, type='track')['tracks']['items']

    if not results:
        return None

    track = results[0]
    return track['album']['images'][0]['url']

def force_cover_update():
    for track in Session.query(Track):
        cover = get_cover_from_spotify(track.title, track.artist)
        if cover and cover != track.cover:
            track.cover = cover
    transaction.commit()

def get_or_create_track(title, artist, album, lastfm_cover):
    track, created = get_or_create(Track, title=title, artist=artist, album=album)
    if created:
        track.cover = get_cover_from_spotify(title, artist) or lastfm_cover
    return track

def update():
    network = pylast.LastFMNetwork(api_key="57ee3318536b23ee81d6b27e36997cde")
    create_db()

    users = Session.query(User).all()
    for user in users:
        current_track = network.get_user(user.username).get_now_playing()
        if current_track:
            title = current_track.title
            artist = current_track.get_artist().name

            a = current_track.get_album()
            if a:
                album = a.title
                cover = a.get_cover_image()
            else:
                album, cover = None, None

            track = get_or_create_track(title, artist, album, cover)

            if user.current_track != track:
                lt = ListenedTrack(user=user, track=track, time=datetime.datetime.now())
                Session.add(lt)
                user.current_track = track
                print('{} is now listening to {}'.format(user.username, title))
        else:
            user.current_track = None

    transaction.commit()
