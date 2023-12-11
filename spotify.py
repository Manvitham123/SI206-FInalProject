import unittest
import sqlite3
import json
import os
import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
cid = '72fbe8b5ea87405286fbc89b66e33d7e'
secret = 'c021da7bc65a4d909e242dc52772637c'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager
=
client_credentials_manager)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

def create_spotify_oauth(client_id, client_secret, redirect_uri):
    scope = "user-top-read"  # Add other scopes as needed
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope
    )

# Use this function to get an authenticated Spotify object
def get_spotify_client(client_id, client_secret, redirect_uri):
    sp_oauth = create_spotify_oauth(client_id, client_secret, redirect_uri)
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print("Please navigate here and authorize:", auth_url)
        response = input("Paste the redirect URL here: ")
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)

    return spotipy.Spotify(auth=token_info['access_token'])

def get_spotify_user_id(sp):
    user_profile = sp.current_user()
    return user_profile['id']

def set_up_database(db_name):
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path + "/" + db_name)
        cur = conn.cursor()
        return cur, conn
 
def search_playlist(sp, query, limit=10):
    results = sp.search(q=query, type='playlist', limit=limit)
    playlists = results['playlists']['items']
    return [(playlist['name'], playlist['id']) for playlist in playlists]

def fetch_top_songs(sp, year, limit=50):
    year = 2020
    playlists = search_playlist(sp, f"Your Top Songs {year}")[0]
    top_songs = []
    name = playlists[0]
    playlist_id = playlists[1] 
    results = sp.playlist_tracks(playlist_id, limit=50, offset=0)
    top_songs = []
    for item in results['items']:
         track = item['track']
         top_songs.append(get_track_features(track['id']))
    return top_songs

def get_track_features(id):
    metadata = sp.track(id)
    features = sp.audio_features(id)

    # metadata
    name = metadata['name']
    album = metadata['album']['name']
    artist = metadata['album']['artists'][0]['name']
    release_date = metadata['album']['release_date']
    length = metadata['duration_ms']
    popularity = metadata['popularity']
    # audio features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    time_signature = features[0]['time_signature']
    track = {"name": name, "album":album, "artist":artist,"release_date":release_date, "length":length, "popularity": popularity, 
             "danceability": danceability,"acousticness": acousticness, " danceability":danceability,"energy": energy,"instrumentalness": instrumentalness,"liveness": liveness, 
            "loudness": loudness,"speechiness": speechiness, "tempo": tempo, "time_signature":time_signature}
    return track



import requests

def fetch_covid_data(api_url, params=None):
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def get_audio_features(sp, track_ids):
    features = sp.audio_features(tracks=track_ids)
    return features

def process_audio_features(audio_features):
    processed_data = []
    for feature in audio_features:
        track_data = {
            'id': feature['id'],
            'danceability': feature['danceability'],
            'energy': feature['energy'],
            'valence': feature['valence'],  # a measure of musical positiveness
            # Add other relevant features
        }
        processed_data.append(track_data)
    return processed_data


def assign_mood(track_data):
    for track in track_data:
        # Example: Define mood based on valence
        if track['valence'] > 0.75:
            track['mood'] = 'Happy'
        elif track['valence'] < 0.25:
            track['mood'] = 'Sad'
        else:
            track['mood'] = 'Neutral'
    return track_data

def get_track_id(sp, title, artist):
    """
    Fetch the Spotify track ID for a given song title and artist.

    Args:
    sp: Spotify API client instance.
    title (str): The title of the song.
    artist (str): The name of the artist.

    Returns:
    str: The Spotify track ID, or None if not found.
    """
    query = f'track:{title} artist:{artist}'
    results = sp.search(q=query, type='track', limit=1)

    items = results['tracks']['items']
    if items:
        # Assuming the first search result is the correct one
        return items[0]['id']
    else:
        return None

import re

def clean_song_name(song_name):
    if '$' in song_name:
        song_name = song_name.replace('$', 's')
    cleaned_name = song_name
    if '(' in song_name:
         cleaned_name = re.sub(r'\([^)]*\)', '', cleaned_name).strip()
    #cleaned_name = re.sub(r'[^\w\s,]', '', song_name)  # Keeps letters, numbers, underscores, and whitespace
    return cleaned_name

def clean_artist_name(artist_name):
    if "Featuring" in artist_name:
            artist_name = artist_name.split(" Featuring")[0]
    if ' x ' in artist_name:
        artist_name = artist_name.replace('x', '&')
    if ' X ' in artist_name:
        artist_name = artist_name.replace('X', '&')
    if ', ' in artist_name:
         artist_name = artist_name.split(",")[0].strip()
    if 'With ' in artist_name:
         artist_name = artist_name.split("With")[0].strip()
    if "Layton Greene" in artist_name:
         artist_name = artist_name.replace('Layton Greene', 'Quality Control')
    return artist_name


def enhance_track_data(sp, track_list):
    enhanced_data = []

    for title, artist, rank in track_list:

        artist = clean_artist_name(artist)
        print(artist)
        print(rank)
        print(title)
        title = clean_song_name(title)
        print(title)
        track_id = get_track_id(sp, title, artist)
        audio_features = get_audio_features(sp, [track_id])
        processed_features = process_audio_features(audio_features)

        if processed_features:
            track_data = processed_features[0]  # Assuming we get one record per track ID
            assign_mood([track_data])

            enhanced_data.append((
                title, 
                artist, 
                rank, 
                track_data['valence'], 
                track_data['danceability'], 
                track_data['energy'], 
                track_data['mood']
            ))

    return enhanced_data
"""
def process_covid_data(covid_data):
    processed_data = []
    for record in covid_data:
        covid_record = {
            'date': record['date'],
            'infections': record['positiveIncrease'],
            # Add other relevant fields
        }
        processed_data.append(covid_record)
    return processed_data

  
def insert_spotify_data(cur,conn, spotify_data):
    cur.execute('''CREATE TABLE IF NOT EXISTS top_songs (
                id TEXT PRIMARY KEY,
                name TEXT,
                artist TEXT,
                album TEXT,
                release_date TEXT
            )''')
    for song in spotify_data:
        cur.execute('INSERT OR IGNORE INTO top_songs (id, name, artist, album, release_date) VALUES (?, ?, ?, ?, ?)',
                  (song['id'], song['name'], song['artist'], song['album'], song['release_date']))
    conn.commit()


def insert_covid_data(cur,conn, covid_data):
    cur.execute('''CREATE TABLE IF NOT EXISTS covid_data (
                date TEXT PRIMARY KEY,
                infections INTEGER
            )''')
    for record in covid_data:
        cur.execute('INSERT OR IGNORE INTO covid_data (date, infections) VALUES (?, ?)',
                  (record['date'], record['infections']))
    conn.commit()

"""
def main():
    sp = get_spotify_client(cid, secret, "https://google.com/")
   # json_covid_data = fetch_covid_data("https://api.covidtracking.com")
    #json_spotify_data = fetch_top_songs(sp,2020)
    #cur1, conn1 = set_up_database("spotify.db")
    #cur, conn = set_up_database("covid.db")
    #insert_covid_data(cur, conn, json_covid_data)
    #insert_spotify_data(cur1, conn1, json_spotify_data)
   # conn1.close()
if __name__ == "__main__":
    main()
   