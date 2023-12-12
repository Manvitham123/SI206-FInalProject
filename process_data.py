import unittest
import sqlite3
import json
import os

import re

# calculate average audio features for 2019 & 2020
def average_song_analysis_features(db_filename):
    # parameter --> pass in database filename 
    # analyze audio features from data tables --> Billboard_Hot_100_2019_Join, Billboard_Hot_100_2020_Join
    # return tuple --> (valence, danceability, energy, mood)


def main():
    average_song_analysis_features('Billboard_Hot_100_Database.db')
    

if __name__ == "__main__":
    main()