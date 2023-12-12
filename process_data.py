import unittest
import sqlite3
import json
import os

import re

# calculate average audio features for 2019 & 2020
def average_song_analysis_features(db_filename, table_2019, table_2020, audio_features_list):

    # return tuple of averages --> (valence, danceability, energy, mood)

    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()

    tuple_average_values_2019 = ()
    tuple_average_values_2020 = ()

    for audio_feature in audio_features_list:
        # data from 2019 table
        query_2019 = f"SELECT AVG({audio_feature}) FROM {table_2019}"
        cur.execute(query_2019)
        average_value_2019 = cur.fetchone()[0]
        tuple_average_values_2019 += (average_value_2019,)

        # data from 2020 table
        query_2020 = f"SELECT AVG({audio_feature}) FROM {table_2020}"
        cur.execute(query_2020)
        average_value_2020 = cur.fetchone()[0]
        tuple_average_values_2020 += (average_value_2020,)

        # tuple --> averages of valence, danceability, energy... get mood by checking the valence level (return mood as str)

    conn.close()
    print(tuple_average_values_2019, tuple_average_values_2020)
    return tuple_average_values_2019, tuple_average_values_2020



def main():
    db_filename = 'Billboard_Hot_100_Database.db'

    table_2019 = 'Billboard_Hot_100_2019_Join'
    table_2020 = 'Billboard_Hot_100_2020_Join'

    # column names from tables
    audio_features_list = ['Valence', 'Danceability', 'Energy', 'Mood']

    average_song_analysis_features(db_filename, table_2019, table_2020, audio_features_list)



if __name__ == "__main__":
    main()