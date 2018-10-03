#!/usr/bin/env python3

import sys
import csv
import matplotlib.pyplot
import numpy
from collections import defaultdict
from os import path
from nltk import tokenize
from pprint import pprint
def numOfArtists(*args):
    """
    returns number of artists/bands in the collection
    """
    return len(art_song)
def numOfSongs(*args):
    """
    returns number of songs in the collection
    """
    sum = 0
    for  key,value in art_song.items():
        sum = sum + len(value)
    return sum
def avgNumOfSongs(*args):
    """
    returns average number of songs per artists/bands in the collection
    """
    return numOfSongs() / numOfArtists()

def avgNumOfWords(*args):
    """
    returns average number of unique words per song in the collection
    """
    sum = 0
    cnt = 0

    return 0
with open("songdata.csv",'r') as csvfile:
    song_data = csv.DictReader(csvfile)
    art_song = defaultdict(list)
    for row in song_data:
        art_song[row['artist']].append(row['song'])

print(numOfArtists())
print(numOfSongs())
print("%d" % avgNumOfSongs())
