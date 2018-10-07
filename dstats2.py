#!/usr/bin/env python3
#prev version
import sys
import csv
import matplotlib.pyplot as plt
import numpy
import re
from collections import defaultdict
from os import path
from nltk import tokenize
from pprint import pprint
#def __init__(self):
   #Initialize dstat with csv fileset to sys.stdin
def numOfArtists(*args):
#returns number of artists/bands in the collection
    return len(art_song)

def numOfSongs(*args):
#returns number of songs in the collection
    sum = 0
    for  key,value in art_song.items():
        sum = sum + len(value)
    return sum
def avgNumOfSongs(*args):
#returns average number of songs per artists/bands in the collection
    return numOfSongs() / numOfArtists()
def unique_num(list_in):
#function that returns number of unique elements in the list

    u_list = []
    for ele in list_in:
        # check if ele is already in unique list
        if ele not in u_list:
            u_list.append(ele)
    # return u_list
    return len(u_list)
def avgNumOfWords(*args):
#returns average number of unique words per song in the collection
    sum = 0
    for key,value in words.items():
        sum = sum + unique_num(value[0])
    return sum / numOfSongs()
def barChart(*args):
    x = []
    y = []
    temp = sorted(art_word.items(),key = lambda k : k[1],reverse = True)[:10]
    for k,v in temp:
        x.append(k)
        y.append(v)
    plt.figure(figsize = (12,5))
    plt.rcParams.update({'font.size': 7})
    plt.bar(x,y)
    plt.suptitle('Top 10 songs with unique number of words')
    plt.show()
    return

song_data = csv.DictReader(sys.stdin)
art_song = defaultdict(list)
words = defaultdict(list)
art_word = defaultdict(int)
for row in song_data:
    art_song[row['artist']].append(row['song'])
    words[row['song']].append(list(filter(None, re.split('[\W+]', row['text']))))
    art_word[row['artist']] += unique_num(words[row['song']])

sorted_art_word = sorted(art_word.items())
print(numOfArtists())
print(numOfSongs())
print("%d" % avgNumOfSongs())
print("%d" % avgNumOfWords())
for item in sorted_art_word:
    print(item[1])
barChart()

#CSVReader reader = new CSVReader(new InputStreamReader(input, "UTF-8")
