import unittest
import sqlite3
import json
import os
import billboard
import re
import matplotlib.pyplot as plt
import csv
from spotify import *
from bs4 import BeautifulSoup
import requests


def create_data_base(database_name):
    db_name = f'{database_name}.db'
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn

def song_table(chart, cur, conn):
    table_name = "song_ids"
    create_table_query = """
    CREATE TABLE IF NOT EXISTS song_ids (
    ID INTEGER PRIMARY KEY,
    Title TEXT,
    Artist TEXT,
    UNIQUE (Title, Artist)
    )"""
    cur.execute(create_table_query)

    for i in range(len(chart)):
            song_title = chart[i].title
            song_artist = chart[i].artist
            cur.execute("""INSERT OR IGNORE INTO song_ids (Title, Artist) 
                        VALUES (?, ?)""", (song_title, song_artist))
    conn.commit()


def billboard_hot_100(date, cur, conn):
    song_list = []
    chart = billboard.ChartData('hot-100', date)
    song_table(chart, cur, conn)
    year = date[:4]  
    table_name = f"Billboard_Hot_100_{year}"
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        SongID INTEGER PRIMARY KEY, 
        Rank INTEGER,
        FOREIGN KEY(SongID) REFERENCES song_ids(ID)
    )"""
    cur.execute(create_table_query)
    cur.execute(f"SELECT MAX(Rank) FROM {table_name}")
    temp = cur.fetchone()[0]

    if not temp:
        index = 0
    else:
        index = int(temp)


    for i in range(index, index + 10):
        song_title = chart[i].title
        song_artist = chart[i].artist
        song_rank = chart[i].rank
        cur.execute("SELECT ID FROM song_ids WHERE Title = ? AND Artist = ?", (song_title, song_artist))
        song_id_result = cur.fetchone()
        if song_id_result:
            song_id = song_id_result[0]
            song_list.append((song_title, song_artist, song_rank, song_id))
            cur.execute(f"INSERT OR IGNORE INTO {table_name} (SongID, Rank) VALUES (?, ?)", (song_id, song_rank))

        conn.commit()

 

    return song_list

       


def main():
    database_name = 'Billboard_Hot_100_Database'
    cur, conn = create_data_base(database_name)
    sp = get_spotify_client(cid, secret, "https://google.com/")
    date_list = ['2019-12-01', '2020-12-01']
    create_mood_table(cur, conn)
    for date in date_list:
        hot_100_songs = billboard_hot_100(date, cur, conn)
        data = enhance_track_data(sp, hot_100_songs)
        insert_spotify_data(cur, conn, data)
        year = date[:4]  
        table_name = f"Billboard_Hot_100_{year}"
        join_spotify_billboard(cur, conn, table_name)
     

if __name__ == "__main__":
    main()


