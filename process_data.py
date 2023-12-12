import unittest
import sqlite3
import json
import os

import re

# calculate average song valence level 
def average_valence(db_filename):
    
    # parameter --> pass in valence output of spotipy function 

# calculate average song danceability level 
def average_danceability(db_filename):

    # parameter --> pass in danceability output of spotipy function

# calculate average song mood level 
def average_mood(db_filename):

    # mood --> pass in mood output of spotipy function


# calculate average song energy level 
def average_energy(db_filename):

    # energy --> pass in energy output of spotipy function



def main():
    average_valence('Billboard_Hot_100_Database.db')
    # tables: Billboard_Hot_100_2019_Join # Billboard_Hot_100_2020_Join 
    average_danceability('Billboard_Hot_100_Database.db')
    average_mood('Billboard_Hot_100_Database.db')
    average_energy('Billboard_Hot_100_Database.db')

if __name__ == "__main__":
    main()