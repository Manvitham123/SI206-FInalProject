import matplotlib.pyplot as plt
import os
import sqlite3
import unittest



def valence_histogram_visualization(db_filename, table_2019, table_2020):


    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    query_2019 = f"SELECT AVG({'Valence'}) FROM {table_2019}"
    cursor.execute(query_2019)
    average_valence_2019 = cursor.fetchone()[0]


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
    plt.scatter(danceability_2020, energy_2020, color='grey', alpha=0.5, label='2020')
    plt.xlabel('Danceability')
    plt.ylabel('Energy')
    plt.title('Comparison of Danceability and Energy Levels in 2019 and 2020')
    plt.legend()
    plt.show()

def danceability_distribution_histogram(db_filename, table_2019, table_2020):
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    query_2019 = f"SELECT Danceability FROM {table_2019}"
    cursor.execute(query_2019)
    danceability_2019 = [row[0] for row in cursor.fetchall()]
    query_2020 = f"SELECT Danceability FROM {table_2020}"
    cursor.execute(query_2020)
    danceability_2020 = [row[0] for row in cursor.fetchall()]
    conn.close()
    plt.hist(danceability_2019, bins=10, alpha=0.5, label='2019')
    plt.hist(danceability_2020, bins=10, alpha=0.5, label='2020')
    plt.xlabel('Danceability')
    plt.ylabel('Frequency')
    plt.title('Distribution of Danceability in 2019 and 2020')
    plt.legend()
    plt.show()



def main():
    db_filename = 'Billboard_Hot_100_Database.db'

    table_2019 = 'Billboard_Hot_100_2019_Join'
    table_2020 = 'Billboard_Hot_100_2020_Join'
    
    valence_histogram_visualization(db_filename,table_2019, table_2020)

    danceability_energy_scatterplot(db_filename,table_2019, table_2020)
    danceability_distribution_histogram(db_filename, table_2019, table_2020)

if __name__ == "__main__":
    main()