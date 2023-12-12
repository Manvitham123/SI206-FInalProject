import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

# visualization --> 
# 1 --> histogram comparing the average valence level of 2019 & 2020 
# 2 --> histogram comparing the average danceability level of 2019 & 2020 
# perceived mood for each song --> valence to mood 

# 2 --> line chart/scatterplot comparing the progression of song valence, danceability, energy level between 2019 and 2020
# val

# def load_billboard_spotipy_data(db):
#     # takes in filename of databse as parameter & returns a nested dict
#     conn = sqlite3.connect(db)
#     cur = conn.cursor()


def valence_histogram_visualization(db_filename):
    # histogram comparing the average valence level of 2019 & 2020

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # table name = average_valence
    cursor.execute("SELECT year, valence_level FROM average_song_analysis_features")
    data = cursor.fetchall()

    # separate data for 2019 & 2020
    data_2019 = [item[1] for item in data if item[0] == '2019']
    data_2020 = [item[1] for item in data if item[0] == '2020']

    conn.close()

    # plot histogram
    plt.hist([data_2019, data_2020], color=['blue', 'gray'], label=['2019', '2020'])
    plt.xlabel('Year')
    plt.ylabel('Valence Level')
    plt.title('Average Valence Levels for Top Songs of 2019 and 2020')
    plt.legend()
    plt.show()

# filename of database = average_valence??
# valence_histogram_visualization('average_valence.db')


def average_audio_features(db_filename):
    # bar plot depicting the average valence, danceability, mood between 2019 and 2020



def main():
    valence_histogram_visualization('average_valence.db')


# as valence increases, how does that influence the rank of the song? 
# x = rank, y = valence. see how the value increases/decreases.
# line gra[h]

if __name__ == "__main__":
    main()