"""
This file parses BillboardLyrics.csv, creating dicts for each song's lyrics,
and writing to songData.csv, a file better suited for the needs of our database

BillboardLyrics.csv: The CSV file downloaded from our source

songData.csv: The CSV file with one line for each word in each song along with
it's frequency in that song

"""

import collections
import csv

# Read from our billboard lyrics file
allLyrics = open('BillboardLyrics.csv', encoding="utf-8")
csv_allLyrics = csv.reader(allLyrics)

dictList = []

# Create a word:count dict for each song's lyrics
for row in csv_allLyrics:
    lyrics = str(row[4]).split()
    c = collections.Counter(lyrics)
    dictList.append(c)

# Write to songData
with open("songData.csv", 'w', newline='',encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    songID = 1

    # A row for each word in each song along with its frequency
    for d in dictList:
        for word, count in d.items():
            writer.writerow([songID, word, count])
        songID += 1
