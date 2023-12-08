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
    song_list = {}
    
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
        song_per_date = []

        song_title = chart[i].title
        song_artist = chart[i].artist
        song_rank = chart[i].rank 
            # tuple
            #song_per_date.append((song_title, song_artist, song_rank))
            #song_list[date] = song_per_date
        cur.execute(f"INSERT OR IGNORE INTO {table_name} (Rank, Title, Artist) VALUES (?,?,?)",
            (song_rank, song_title, song_artist)) 

        conn.commit()
       


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
## downloading a chart ##
# ChartData --> constructor to download chart
# e.g. ChartData(name, date=None, year=None, fetch=True, timeout=25)
#
# arguments:
# !!! name – The chart name, e.g. 'hot-100' or 'pop-songs'.
# !!! date – The chart date as a string, in YYYY-MM-DD format. By default, the latest chart is fetched.
# year – The chart year, if requesting a year-end chart. Must be a string in YYYY format. Cannot supply both date and year.
# fetch – A boolean indicating whether to fetch the chart data from Billboard.com immediately (at instantiation time). If False, the chart data can be populated at a later time using the fetchEntries() method.
# max_retries – The max number of times to retry when requesting data (default: 5).
# timeout – The number of seconds to wait for a server response. If None, no timeout is applied.
#
# e.g. to download the Alternative Songs year-end chart for 2006: chart = billboard.ChartData('alternative-songs', year=2006)



## accessing chart entries ##
# If chart is a ChartData instance, we can ask for its entries attribute to get the chart entries (see below) as a list.
# For convenience, chart[x] is equivalent to chart.entries[x], and ChartData instances are iterable.


## chart entry attributes ##
# A chart entry (typically a single track) is of type ChartEntry. A ChartEntry instance has the following attributes:
# !!! title – The title of the track.
# !!! artist – The name of the artist, as formatted on Billboard.com.
# image – The URL of the image for the track.
# peakPos – The track's peak position on the chart as of the chart date, as an int (or None if the chart does not include this information).
# lastPos – The track's position on the previous week's chart, as an int (or None if the chart does not include this information). This value is 0 if the track was not on the previous week's chart.
# weeks – The number of weeks the track has been or was on the chart, including future dates (up until the present time).
# !!! rank – The track's current position on the chart.
# isNew – Whether the track is new to the chart.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def main():
    # create_data_base --> create database for billboard data
    database_name = 'Billboard_Hot_100_Database'
    cur, conn = create_data_base(database_name)
    

    # billboard_hot_100()
    date_list = ['2019-12-01', '2020-12-01']
    for date in date_list:
        hot_100_songs = billboard_hot_100(date, cur, conn)
    

main()


