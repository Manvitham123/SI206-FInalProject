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
    scope = "user-top-read" 
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

def set_up_database(db_name):
        path = os.path.dirname(os.path.abspath(__file__))
        conn = sqlite3.connect(path + "/" + db_name)
        cur = conn.cursor()
        return cur, conn
 
def get_track_features(id):
    metadata = sp.track(id)
    features = sp.audio_features(id)
    name = metadata['name']
    album = metadata['album']['name']
    artist = metadata['album']['artists'][0]['name']
    release_date = metadata['album']['release_date']
    length = metadata['duration_ms']
    popularity = metadata['popularity']
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
            'valence': feature['valence'], 

        }
        processed_data.append(track_data)
    return processed_data

def create_mood_table(cur, conn):
    cur.execute('''CREATE TABLE IF NOT EXISTS Mood (
                    MoodName TEXT PRIMARY KEY,
                    MoodValue INTEGER
                )''')
    moods = [('Happy', 1), ('Neutral', 2), ('Sad', 3)]
    for mood in moods:
        cur.execute('INSERT OR IGNORE INTO Mood (MoodName, MoodValue) VALUES (?, ?)', mood)
    conn.commit()

def assign_mood(track_data):
    for track in track_data:
        if track['valence'] > 0.75:
            #track['mood'] = 'Happy'
            track['mood'] = 1
        elif track['valence'] < 0.50:
            #track['mood'] = 'Sad'
            track['mood'] = 2
        else:
            #track['mood'] = 'Neutral'
            track['mood'] = 3
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

    for title, artist, rank, id in track_list:
        artist = clean_artist_name(artist)
        title = clean_song_name(title)
        track_id = get_track_id(sp, title, artist)
        audio_features = get_audio_features(sp, [track_id])
        processed_features = process_audio_features(audio_features)

        if processed_features:
            track_data = processed_features[0] 
            assign_mood([track_data])


            enhanced_data.append((
                id,
                rank, 
                title, 
                artist, 
                track_data['valence'], 
                track_data['danceability'], 
                track_data['energy'], 
                track_data['mood']
            ))

    return enhanced_data
  
def insert_spotify_data(cur,conn, spotify_data):

    cur.execute('''CREATE TABLE IF NOT EXISTS Song_Analysis (
                SongID TEXT PRIMARY KEY,
                Rank INTEGER,
                Name TEXT,
                Artist TEXT,
                Valence FLOAT,
                Danceability FLOAT,
                Energy  FLOAT,
                Mood FLOAT
            )''')
    
    for song in spotify_data:
        cur.execute('INSERT OR IGNORE INTO Song_Analysis  (SongID, Rank, Name, Artist, Valence, Danceability, Energy, Mood) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                  song)
    conn.commit()

def join_spotify_billboard(cur, conn, billboard_table_name):
    join_table_name = billboard_table_name + "_Join"

    cur.execute(f'''CREATE TABLE IF NOT EXISTS {join_table_name} (
                   SongID TEXT PRIMARY KEY,
                   Rank INTEGER,
                   Valence FLOAT,
                   Danceability FLOAT,
                   Energy FLOAT,
                   Mood FLOAT
               )''')
    cur.execute(f"SELECT MAX(SongID) FROM {join_table_name}")
    last_id_result = cur.fetchone()
    last_id = last_id_result[0] if last_id_result else None
    next_id_condition = "WHERE b.SongID > ?" if last_id else ""
    next_id_values = (last_id,) if last_id else ()

    cur.execute(f'''INSERT INTO {join_table_name} (SongID, Rank, Valence, Danceability, Energy, Mood)
                    SELECT b.SongID, b.Rank, s.Valence, s.Danceability, s.Energy, s.Mood
                    FROM {billboard_table_name} b
                    INNER JOIN Song_Analysis s ON b.SongID = s.SongID
                    {next_id_condition}
                    ON CONFLICT(SongID) DO NOTHING''', next_id_values)
    conn.commit()

    

def main():
    sp = get_spotify_client(cid, secret, "https://google.com/")
if __name__ == "__main__":
    main()
   