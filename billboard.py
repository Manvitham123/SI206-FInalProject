import unittest
import sqlite3
import json
import os
import billboard


# def billboard_hot_100():
#     # hot 100 songs --> song name, song ranking, artist, (song id??)
#     chart_data = billboard.ChartData('hot-100')
#     hot_100_data = []
#     for i in range(0,len(chart_data)):
#         song_name = chart_data[1].title
#         #song_id = chart_data[]
#         song_ranking = chart_data[1].rank
#         song_artist = chart_data[1].artist


# info needed: song name, ranking, artist, (song id??)

# top 100 songs during Dec 2019 (e.g. Dec 1, 2019) & Dec 2020 (e.g. Dec 1, 2020)

# sort the data so that it's the top 25 songs (then 50, 75, 100) --> store 25 items in the database for each run



## downloading a chart ##
# ChartData --> constructor to download chart
# e.g. ChartData(name, date=None, year=None, fetch=True, timeout=25)
#
# arguments:
# !!! name – The chart name, e.g. 'hot-100' or 'pop-songs'.
# !!! date – The chart date as a string, in YYYY-MM-DD format. By default, the latest chart is fetched.
# year – The chart year, if requesting a year-end chart. Must be a string in YYYY format. Cannot supply both date and year.
# fetch – A boolean indicating whether to fetch the chart data from Billboard.com immediately (at instantiation time). If False, the chart data can be populated at a later time using the fetchEntries() method.
# max_retries – The max number of times to retry when requesting data (default: 5).
# timeout – The number of seconds to wait for a server response. If None, no timeout is applied.
#
# e.g. to download the Alternative Songs year-end chart for 2006: chart = billboard.ChartData('alternative-songs', year=2006)



## accessing chart entries ##
# If chart is a ChartData instance, we can ask for its entries attribute to get the chart entries (see below) as a list.
# For convenience, chart[x] is equivalent to chart.entries[x], and ChartData instances are iterable.


## chart entry attributes ##
# A chart entry (typically a single track) is of type ChartEntry. A ChartEntry instance has the following attributes:
# !!! title – The title of the track.
# !!! artist – The name of the artist, as formatted on Billboard.com.
# image – The URL of the image for the track.
# peakPos – The track's peak position on the chart as of the chart date, as an int (or None if the chart does not include this information).
# lastPos – The track's position on the previous week's chart, as an int (or None if the chart does not include this information). This value is 0 if the track was not on the previous week's chart.
# weeks – The number of weeks the track has been or was on the chart, including future dates (up until the present time).
# !!! rank – The track's current position on the chart.
# isNew – Whether the track is new to the chart.
