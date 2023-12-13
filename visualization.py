import matplotlib.pyplot as plt
import os
import sqlite3
import unittest



def valence_histogram_visualization(db_filename, table_2019, table_2020):
    # histogram comparing the average valence level of 2019 & 2020

    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # average valence level for 2019
    query_2019 = f"SELECT AVG({'Valence'}) FROM {table_2019}"
    cursor.execute(query_2019)
    average_valence_2019 = cursor.fetchone()[0]

    # average valence level for 2020
    query_2020 = f"SELECT AVG({'Valence'}) FROM {table_2020}"
    cursor.execute(query_2020)
    average_valence_2020 = cursor.fetchone()[0]

    data = cursor.fetchall()

    conn.close()

    # plot histogram
    years = ['2019', '2020']
    average_valence_values = [average_valence_2019, average_valence_2020]

    plt.bar(years, average_valence_values, color=['blue', 'gray'])
    plt.xlabel('Year')
    plt.ylabel('Average Valence Level')
    plt.title('Average Valence Levels for 2019 and 2020')
    plt.show()


def 


# 2 --> line chart/scatterplot comparing the progression of song valence, danceability, energy level between 2019 and 2020
# def average_audio_features(db_filename, table_2019, table_2020):
#     # bar plot depicting the average valence, danceability, mood between 2019 and 2020
#     conn = sqlite3.connect(db_filename)
#     cursor = conn.cursor()

#     # average values for 2019
#     query_2019 = f"SELECT AVG(({'Valence'}), AVG({'Danceability'}), AVG({'Energy'})) FROM {table_2019}"
#     cursor.execute(query_2019)
#     average_values_2019 = cursor.fetchone()

#     # average values for 2020
#     query_2020 = f"SELECT AVG(({'Valence'}), AVG({'Danceability'}), AVG({'Energy'})) FROM {table_2020}"
#     cursor.execute(query_2020)
#     average_values_2020 = cursor.fetchone()

#     conn.close()

#     # data to be plotted
#     years = ['2019', '2020']
#     valence = [average_values_2019[0], average_values_2020[0]]
#     danceability = [average_values_2019[1], average_values_2020[1]]
#     energy = [average_values_2019[2], average_values_2020[2]]

#     # line plot
#     plt.plot(years, valence, marker='o', linestyle='-', color='blue', label='Valence')
#     plt.plot(years, danceability, marker='o', linestyle='-', color='grey', label='Danceability')
#     plt.plot(years, energy, marker='o', linestyle='-', color='black', label='Energy')

#     plt.xlabel('Year')
#     plt.ylabel('Average Level')
#     plt.title('Average Valence, Danceability, and Energy Levels for 2019 and 2020')
#     plt.legend()
#     plt.grid(True)
#     plt.show()



def main():
    db_filename = 'Billboard_Hot_100_Database.db'

    table_2019 = 'Billboard_Hot_100_2019_Join'
    table_2020 = 'Billboard_Hot_100_2020_Join'
    
    valence_histogram_visualization(db_filename,table_2019, table_2020)

    average_audio_features(db_filename, table_2019, table_2020)



# as valence increases, how does that influence the rank of the song? 
# x = rank, y = valence. see how the value increases/decreases.
# line gra[h]

if __name__ == "__main__":
    main()