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

        if audio_feature == "Valence": 
            if average_value_2019 > 0.75:
               tuple_average_values_2019 += ('Happy',)
                
            elif average_value_2019 < 0.50:
                tuple_average_values_2019 += ('Sad',)
             
            else:
                tuple_average_values_2019 += ('Neutral',)
            
            if average_value_2020 > 0.75:
               tuple_average_values_2020 += ('Happy',)
                
            elif average_value_2020 < 0.50:
                tuple_average_values_2020 += ('Sad',)
            
            else:
                tuple_average_values_2020 += ('Neutral',)
    

        # tuple --> averages of valence, danceability, energy... get mood by checking the valence level (return mood as str)
        
        # mood --> check valence level --> assign_mood function !
        

# def assign_mood(track_data):
#     for track in track_data:
#         if track['valence'] > 0.75:
#             #track['mood'] = 'Happy'
#             track['mood'] = 1
#         elif track['valence'] < 0.25:
#             #track['mood'] = 'Sad'
#             track['mood'] = 2
#         else:
#             #track['mood'] = 'Neutral'
#             track['mood'] = 3
#     return track_data

    conn.close()
    
    print(tuple_average_values_2019, tuple_average_values_2020)
    return tuple_average_values_2019, tuple_average_values_2020



def main():
    db_filename = 'Billboard_Hot_100_Database.db'

    table_2019 = 'Billboard_Hot_100_2019_Join'
    table_2020 = 'Billboard_Hot_100_2020_Join'

    # column names from tables
    # audio_features_list = ['Valence', 'Danceability', 'Energy', 'Mood']
    audio_features_list = ['Valence', 'Danceability', 'Energy']

    average_song_analysis_features(db_filename, table_2019, table_2020, audio_features_list)



if __name__ == "__main__":
    main()