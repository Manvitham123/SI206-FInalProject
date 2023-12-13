import unittest
import sqlite3
import json
import os
import re

def average_song_analysis_features(db_filename, table_2019, table_2020, audio_features_list):
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

    
    conn.close()
    return tuple_average_values_2019, tuple_average_values_2020

def write_to_output_file(tuple_2019, tuple_2020, audio_features_list, output_filename):
    with open(output_filename, 'w') as file:
        header_features_list = audio_features_list.copy()
        header_features_list.insert(1, 'Mood')
        file.write("Year, " + ", ".join(header_features_list) + "\n")
        data_2019 = "2019, " + ", ".join(map(str, tuple_2019)) + "\n"
        file.write(data_2019)
        data_2020 = "2020, " + ", ".join(map(str, tuple_2020)) + "\n"
        file.write(data_2020)



def main():
    db_filename = 'Billboard_Hot_100_Database.db'

    table_2019 = 'Billboard_Hot_100_2019_Join'
    table_2020 = 'Billboard_Hot_100_2020_Join'

    audio_features_list = ['Valence', 'Danceability', 'Energy']
    average_2019, average_2020 = average_song_analysis_features(db_filename, table_2019, table_2020, audio_features_list)
    write_to_output_file(average_2019, average_2020, audio_features_list, "ProcessedData.txt")



if __name__ == "__main__":
    main()