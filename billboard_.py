import unittest
import sqlite3
import json
import os
import billboard
import re
import matplotlib.pyplot as plt
import csv

from bs4 import BeautifulSoup
import requests


def create_data_base(database_name):
    db_name = f'{database_name}.db'
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    return cur, conn


def billboard_hot_100(date, cur, conn):
    song_list = []
    
    chart = billboard.ChartData('hot-100', date)

        # rank, song title, artist
        # cur --> where you specify what you want it to do
    year = date[:3]
    table_name = f"Billboard_Hot_100_{year}"  # concatenate the table name w/ the date variable
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (Rank NUMBER PRIMARY KEY, Title TEXT, Artist TEXT)"
    cur.execute(create_table_query)
    # conn.commit()


    cur.execute(f"SELECT MAX(Rank) FROM {table_name}")
    temp = cur.fetchone()[0]
    print(temp)
    if not temp:
        index = 0
    else:
        index = int(temp)
        #   print(index)
        # info about top 100 songs
    for i in range(index,index+25):
        #song_per_date = []
        song_title = chart[i].title
        song_artist = chart[i].artist
        song_rank = chart[i].rank 
            # tuple
        song_list.append((song_title, song_artist, song_rank))
            #song_list[date] = song_per_date
        cur.execute(f"INSERT OR IGNORE INTO {table_name} (Rank, Title, Artist) VALUES (?,?,?)",
            (song_rank, song_title, song_artist)) 

        conn.commit()
    return song_list

       


def main():
    # create_data_base --> create database for billboard data
    database_name = 'Billboard_Hot_100_Database'
    cur, conn = create_data_base(database_name)
    # billboard_hot_100()
    date_list = ['2019-12-01', '2020-12-01']
    for date in date_list:
        hot_100_songs = billboard_hot_100(date, cur, conn)
        print(hot_100_songs)
    

main()


