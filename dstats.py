#!/usr/bin/env python3
#In docker running start.sh will download necessary python libraries
#which are matplotlib, nltk, nltk corpus(for stopwords)
#below : codes for start.sh and 1 other file for running start.sh

#start.sh:
#ROOT="$(dirname "${BASH_SOURCE[0]}")"
#
#cd "$ROOT"
#source "$ROOT/pyinstall.sh"
#[[ $# -gt 0 ]] && exec "$@"

#where pyinstall.sh:
#if [[ -f ./requirements.txt ]]; then
#  pip install --no-cache-dir -r ./requirements.txt
#else
#  pip install matplotlib
#  pip install nltk
#  pip install nltk corpus
#  pip freeze > requirements.txt
#fi

#for sys input
import sys
#for saving barChart
import os
#for csv file process\
import csv
#matplot for barchart plotting
import matplotlib.pyplot as plt

#defaultdict to store processed inputs
from collections import defaultdict
#Regexp to process lyric words removing punctuations
#stopwords to remove common high frequency english words with low values
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
#directory of current file
__dirpath__ = os.path.dirname(__file__)
def unique_set(list_in):
#in: list with potential redundancy
#return: list with unique elements

    u_set = set()
    for ele in list_in:
        # check if ele is already in unique list
        if ele not in u_set:
            u_set.add(ele)
    return u_set
def check_nltk(*args):
    import nltk
    try:
        nltk.data.find('stopwords')
        return
    except LookupError:
        nltk.download('stopwords')

def token_words(lyric):
#in: lyric(element of row['text'])
#return: list of words in the lyric
#that is not punctuation & stopwords(nltk.stopwords)
    lyric = lyric.lower()
    #tokenizer that will tokenize lyric('text') into words without punctuation
    #will split aphostrophe words into 2 seperate words but its okay as we only care about full words
    # e.g : would've = would ve but this is fine as we know stopwords will remove ve
    # tweetTokenizer was producing very irregular words in lyric such as (8, numbers and was dist

    #tokenize word into alphabets only
    tokenizer = RegexpTokenizer(r'[a-z]+')
    #apply tokenizer
    words = tokenizer.tokenize(lyric)
    #convert list of stopwords to set of stopwords for faster access
    en_stopwords = set(stopwords.words('english'))

    #we remove stopwords in words
    words_lyric = [w for w in words if not w in en_stopwords]
    return words_lyric

def process(songcsv):
#in: csvDictReader(csvfile)
#return: these are returned in sinlge function to reduce repeated csv read
#        set of unique artists
#        dictionary of artist : number of songs by artist
#                      artist : sum of unique words in all songs
#                      artist : number of unique words in all songs(By artist)
    u_art = set()
    art_count = defaultdict(int)
    song_word = defaultdict(int)
    art_word = defaultdict(int)
    for row in songcsv:
        words = token_words(row['text'])
        unique_words = len(unique_set(words))
        #'link' is used as index instead of 'song'(title) as there might be a duplicate name for 'song'
        song_word[row['link']] += unique_words
        art_word[row['artist']] += unique_words
        art_count[row['artist']] += 1

        if row['artist'] not in u_art:
            u_art.add(row['artist'])
    return u_art,art_count,song_word,art_word

def barChart(art_avg,out_file):
#in: Dictionary of artist : average unique words in songs by artist
#saves barChart that displays top 10 artists with unique words in out_file
#return: none
    x = []
    y = []
    #Take first 10 elements of sorted art_avg ( artist : average number of songs)
    #that is in descending order, sorted by value(average number of songs)
    temp = sorted(art_avg.items(),key = lambda k : k[1],reverse = True)[:10]
    #add these key,value ( artist : average number of songs) to x and y axies
    for k,v in temp:
        x.append(k)
        y.append(v)
    plt.figure(figsize = (12,5))
    plt.rcParams.update({'font.size': 7})
    plt.bar(x,y)
    plt.suptitle('Top 10 songs with unique number of words')
    plt.savefig(out_file)
    return

def main():
    song_data = csv.DictReader(sys.stdin)
    unique_artist,art_count,song_word,art_word = process(song_data)
    art_avg = defaultdict(int)
    sorted_avg = []
    for key in art_word:
        art_avg[key] = art_word[key] / art_count[key]
        sorted_avg = sorted(art_avg.items(), key = lambda x: x[0])

    print("Number of artists in the collection: %d" % len(unique_artist))

    print("Number of songs in the collection: %d" % len(song_word))

    sum = 0
    temp = 0
    for key in song_word:
        sum += song_word[key]
        temp = sum / len(song_word)
    #print only 5 digits after decmial points.
    print("Average number of unique words per song in the collection:", round(temp,5))

    print("Average number of unique words per song of an artist in the collection:")
    for v in sorted_avg:
        print("%d" % v[1])
    #saving barChart as form filename.fileformat
    f_output  = os.path.join(__dirpath__, './barChart.png')

    barChart(art_avg,f_output)

if __name__ == "__main__":
    main()
