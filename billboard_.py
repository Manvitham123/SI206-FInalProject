import unittest
import sqlite3
import json
import os
import billboard
import re
import matplotlib.pyplot as plt
import csv
#import spotify.py

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
        try:
            song_title = chart[i].title
            song_artist = chart[i].artist
            cur.execute("""INSERT OR IGNORE INTO song_ids (Title, Artist) 
                        VALUES (?, ?)""", (song_title, song_artist))
        except Exception as e:
            print(f"An error occurred: {e}")

    conn.commit()

def billboard_hot_100(date, cur, conn):
    song_list = []
    chart = billboard.ChartData('hot-100', date)
    song_table(chart, cur, conn)
    year = date[:4]  # Get the full year
    table_name = f"Billboard_Hot_100_{year}"
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        Rank INTEGER PRIMARY KEY, 
        SongID INTEGER,
        FOREIGN KEY(SongID) REFERENCES song_ids(ID)
    )"""
    cur.execute(create_table_query)
    cur.execute(f"SELECT MAX(Rank) FROM {table_name}")
    temp = cur.fetchone()[0]
    print(temp)
    if not temp:
        index = 0
    else:
        index = int(temp)
        print(index)

    for i in range(index, index + 25):
        song_title = chart[i].title
        song_artist = chart[i].artist
        song_rank = chart[i].rank
        cur.execute("SELECT ID FROM song_ids WHERE Title = ? AND Artist = ?", (song_title, song_artist))
        song_id_result = cur.fetchone()

        if song_id_result:
            song_id = song_id_result[0]
            # Insert the data into the Billboard_Hot_100_{year} table
            cur.execute(f"INSERT OR IGNORE INTO {table_name} (Rank, SongID) VALUES (?, ?)", (song_rank, song_id))

        conn.commit()

    # ... (rest of your function)

    return song_list

       


def main():
    # create_data_base --> create database for billboard data
    database_name = 'Billboard_Hot_100_Database'
    cur, conn = create_data_base(database_name)
    # billboard_hot_100()
    date_list = ['2019-12-01', '2020-12-01']
    # date_list = ['2019-12-01', '2020-04-01']
    for date in date_list:
        hot_100_songs = billboard_hot_100(date, cur, conn)
        print(hot_100_songs)
    

main()


