import matplotlib.pyplot as plt
import os
import sqlite3




def valence_histogram_visualization(db_filename, table_2019, table_2020):
    conn = sqlite3.connect(db_filename)
    cur = conn.cursor()
    query_2019 = f"SELECT AVG({'Valence'}) FROM {table_2019}"
    cur.execute(query_2019)
    average_valence_2019 = cur.fetchone()[0]
    query_2020 = f"SELECT AVG({'Valence'}) FROM {table_2020}"
    cur.execute(query_2020)
    average_valence_2020 = cur.fetchone()[0]
    data = cur.fetchall()
    conn.close()
    years = ['2019', '2020']
    average_valence_values = [average_valence_2019, average_valence_2020]
    plt.bar(years, average_valence_values, color=['blue', 'gray'])
    plt.xlabel('Year')
    plt.ylabel('Average Valence Level')
    plt.title('Average Valence Levels for 2019 and 2020')
    plt.show()


<<<<<<< HEAD
# 2 --> line chart/scatterplot comparing the progression of song valence, danceability, energy level between 2019 and 2020
def average_audio_features(db_filename, table_2019, table_2020):
    # bar plot depicting the average valence, danceability, mood between 2019 and 2020
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()

    # average values for 2019
    query_2019 = f"SELECT AVG(({'Valence'}), AVG({'Danceability'}), AVG({'Energy'})) FROM {table_2019}"
    cursor.execute(query_2019)
    average_values_2019 = cursor.fetchone()

    # average values for 2020
    query_2020 = f"SELECT AVG(({'Valence'}), AVG({'Danceability'}), AVG({'Energy'})) FROM {table_2020}"
    cursor.execute(query_2020)
    average_values_2020 = cursor.fetchone()

    conn.close()

    # data to be plotted
    years = ['2019', '2020']
    valence = [average_values_2019[0], average_values_2020[0]]
    danceability = [average_values_2019[1], average_values_2020[1]]
    energy = [average_values_2019[2], average_values_2020[2]]

    # line plot
    plt.plot(years, valence, marker='o', linestyle='-', color='blue', label='Valence')
    plt.plot(years, danceability, marker='o', linestyle='-', color='grey', label='Danceability')
    plt.plot(years, energy, marker='o', linestyle='-', color='black', label='Energy')

    plt.xlabel('Year')
    plt.ylabel('Average Level')
    plt.title('Average Valence, Danceability, and Energy Levels for 2019 and 2020')
    plt.legend()
    plt.grid(True)
    plt.show()

=======
def danceability_energy_scatterplot(filename, table_2019, table_2020):
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    query_2019 = f"SELECT Danceability, Energy FROM {table_2019}"
    cur.execute(query_2019)
    data_2019 = cur.fetchall()
    query_2020 = f"SELECT Danceability, Energy FROM {table_2020}"
    cur.execute(query_2020)
    data_2020 = cur.fetchall()
    conn.close()
    danceability_2019 = [item[0] for item in data_2019]
    energy_2019 = [item[1] for item in data_2019]
    danceability_2020 = [item[0] for item in data_2020]
    energy_2020 = [item[1] for item in data_2020]
    plt.figure(figsize=(10, 6))
    plt.scatter(danceability_2019, energy_2019, color='blue', alpha=0.5, label='2019')
    plt.scatter(danceability_2020, energy_2020, color='yellow', alpha=0.5, label='2020')
    plt.xlabel('Danceability')
    plt.ylabel('Energy')
    plt.title('Comparison of Danceability and Energy Levels in 2019 and 2020')
    plt.legend()
    plt.show()
>>>>>>> 54710d7ff852038c7f3613144f70a9aad0bae486


def main():
    db_filename = 'Billboard_Hot_100_Database.db'
    table_2019 = 'Billboard_Hot_100_2019_Join'
    table_2020 = 'Billboard_Hot_100_2020_Join'
    valence_histogram_visualization(db_filename,table_2019, table_2020)
    danceability_energy_scatterplot(db_filename,table_2019, table_2020)

    average_audio_features(db_filename, table_2019, table_2020)


if __name__ == "__main__":
    main()