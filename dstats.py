#!/usr/bin/env python3

import sys
import csv
import matplotlib.pyplot as plt
import numpy
import re
from collections import defaultdict
from os import path
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
def process(songcsv):
    u_art = []
    art_count = defaultdict(int)
    song_word = defaultdict(int)
    art_word = defaultdict(int)
    for row in songcsv:
        words = token_words(row['text'])
        unique_words = unique_set(words)
        song_word[row['link']] += unique_words
        art_word[row['artist']] += unique_words
        art_count[row['artist']] += 1
        if row['artist'] not in u_art:
            u_art.append(row['artist'])
#returns set of unique artists
#       dictionary of art : number of songs by artist
#               artist : sum of unique words in all songs
#               artist : number of unique words in all songs(By artist)

    return u_art,art_count,song_word,art_word


def unique_set(list_in):
#returns number of unique elements in the list
    u_set = []
    for ele in list_in:
        # check if ele is already in unique list
        if ele not in u_set:
            u_set.append(ele)
    # return u_list
    return len(u_set)

def token_words(lyric):
#returns list of words in the lyric
#that is not punctuation & stopwords(nltk.stopwords)
    lyric = lyric.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(lyric)
    en_stopwords = set(stopwords.words('english'))
    words_lyric = [w for w in words if not w in en_stopwords]
    return words_lyric

def barChart(art_avg):
    x = []
    y = []
    temp = sorted(art_avg.items(),key = lambda k : k[1],reverse = True)[:10]
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
unique_artist,art_count,song_word,art_word = process(song_data)
art_avg = defaultdict(int)
for key in art_word:
    art_avg[key] = art_word[key] / art_count[key]
sorted_avg = sorted(art_avg.items(), key = lambda x: x[0])

print("Number of artists in the collection: %d" % len(unique_artist))

print("Number of songs in the collection: %d" % len(song_word))

#print("Average number of songs per artists/bands in the collection: %d" % (len(unique_artist)/len(song_word)))
sum = 0
for key in song_word:
    sum += song_word[key]
temp = sum / len(song_word)
print("Average number of unique words per song: %d" % temp)

print("Average number of unique words per song of an artist:")
for v in sorted_avg:
    print("%d" % v[1])
barChart(art_avg)
