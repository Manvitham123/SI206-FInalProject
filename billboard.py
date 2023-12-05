import unittest
import sqlite3
import json
import os
import billboard


def billboard_hot_100():
    # hot 100 songs --> song name, song id, song ranking, artist
    chart_data = billboard.ChartData('hot-100')
    hot_100_data = []
    for i in range(0,len(chart_data)):
        song_name = chart_data[1].title
        #song_id = chart_data[]
        song_ranking = chart_data[1].rank
        song_artist = chart_data[1].artist

