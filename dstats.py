#!/usr/bin/env python3
"""
#In docker running start.sh will download necessary python libraries
#which are matplotlib, nltk, nltk corpus(for stopwords)
#below : codes for start.sh and 1 other file for running start.sh

#start.sh:
#ROOT="$(dirname "${BASH_SOURCE[0]}")"
#
#cd "$ROOT"
#source "$ROOT/pyinstall.sh"

#where pyinstall.sh:
#if [[ -f ./requirements.txt ]]; then
#  pip install --no-cache-dir -r ./requirements.txt
#else
#  pip install matplotlib
#  pip install nltk
#  pip freeze > requirements.txt
#fi
"""
#this is for building regular expression
from string import ascii_lowercase
#re for errortesting
import re
#for sys input
import sys
#for saving barChart
import os
#for csv file process\
import csv
#matplot for barchart plotting
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pprint import pprint
#defaultdict to store processed inputs
from collections import defaultdict
#stopwords to remove common high frequency english words with low values
from nltk.tokenize.regexp import RegexpTokenizer
from nltk.corpus import stopwords
#directory of current file
__dirpath__ = os.path.dirname(__file__)
def unique_set(list_in):
    """
    in: list with potential redundancy
    return: list with unique elements
    """
    u_set = set()
    for ele in list_in:
        # check if ele is already in unique list
        if ele not in u_set:
            u_set.add(ele)
    return u_set

def token_words(lyric):
    """
    in: lyric(element of row['text'])
    return: list of words in the lyric
    that is not punctuation & stopwords
    """
    lyric = lyric.lower()
    """
     tokenizer that will tokenize lyric('text') into words without punctuation
     will split aphostrophe words into 2 seperate words but its okay as we only care about full words
     e.g : would've = would ve but this is fine as we know stopwords will remove ve
     tweetTokenizer was producing very irregular words in lyric such as (8, numbers and was dist
    """
    #apply tokenizer
    tokenizer1= RegexpTokenizer("[a-z]+")
    words = tokenizer1.tokenize(lyric)
    #convert list of stopwords to set of stopwords for faster access
    en_stopwords = set(stopwords.words('english'))
    #we remove stopwords in words
    #and add few words that were in the words_lyric for cleaner process
    en_stopwords.add('chorus')

    words_lyric = [w for w in words if not w in en_stopwords]

    #this is for me to see if there is anything that doens't follow regexp
    #f = open("errortext.txt", "w")
    #regexp = re.compile("\w+'\w+")
    #regexp2 = re.compile("ya+")
    #errorwords = [w for w in words_lyric if regexp2.match(w)]
    #for w in errorwords:
    #    f.write(w)
    #    f.write("\n")
    words_lyric = postProcess(words_lyric)

    return words_lyric

def process(songcsv):
    """
    in: csvDictReader(csvfile)
    return: these are returned in sinlge function to reduce repeated csv read
            set of unique artists
            dictionary of artist : number of songs by artist
                          artist : sum of unique words in all songs
                          artist : number of unique words in all songs(By artist)
    """
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

def postProcess(lyric):
    """
    in : lyric(in a form of list) that requires postProcessing, set of words in document so far for reference
    Words are processed in following ways
    1. word that has repetitive letters such as 'ya', 'yaaa' into single form('ya')
    2. for words that has length > 3 (if word length is greater than 4 usually 1 letter at the end does not change the meaning)
        if words - words.last or worst + [a-z] gives us a match with one of
    out: lyric into document
    """

    f = open("replacedtext.txt", "a")

    cnt = 0

    n_lyric = removerepeat(lyric,f)
    n2_lyric = removeNonWord(n_lyric,f)
    return n2_lyric

#this function was not used due to time issue
#it was taking O(n^2) per lyric and was bottlenecking tokenizer even worse
def reducerepeat(word,lyric,file):
    """
    in : word to be compared ,whole lyric, file for result output for debuggin
    return : lyric with no repeated words

    apply regular expressions (word)+ and word(word.lastcharacter)+ to all lyrics and replace them with
    smaller word
    """
    for w in lyric:
    #if is not the same word, we want to see if this word is repetitive form of word we have
        if word != w:
            regexp = re.compile('(%s)+' % word)
            regexp2 = re.compile('%s(%s)+' % (word, word[-1]))

            if regexp.match(w):
                if(regexp.match(w).span()[1] == len(w)):
                    file.write("changed %s to %s \n" % (word,w))
                    lyric.remove(w)
                    lyric.append(word)

                elif regexp2.match(w):
                    if(regexp.match(w).span()[1] == len(w)):
                        file.write('changed %s to %s \n' % (word,w))
                        lyric.remove(w)
                        lyric.append(word)
    return lyric
def removeNonWord(lyric,file):
    """
    in : word to be compared ,whole lyric, file for result output for debuggin
    return : lyric with no repeated words

    apply regular expressions [aeuio]+ to make sure
    """
    for w in lyric:
        regexp = re.compile('[aeuio]')
        match = regexp.search(w)
        if not match:
            lyric.remove(w)
            file.write("this word %s is one without vowels\n" % w)
    return lyric
def removerepeat(lyric,file):
    """
    in : word to be compared ,whole lyric, file for result output for debuggin
    return : lyric with no repeated words

    apply regular expressions all alphabet+
    """
    #regstr is all repetition of single alphabet
    regstr =""
    for c in ascii_lowercase:
        regstr = regstr+ c+'+'+'|'
    regstr = regstr[:-1]
    regexp = re.compile(regstr)
    n_lyric = lyric
    for w in lyric:
        match = regexp.match(w)
        if match:
            if match.span()[1] == len(w):
                n_lyric.remove(w)
    return n_lyric

def barChart(art_avg,out_file):
    """
    in: Dictionary of artist : average unique words in songs by artist , file with write option
    saves barChart that displays top 10 artists with unique words in out_file
    return: none
    """
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
        print("{0:>25s} : {1:>8f}".format(v[0],v[1]))
    #saving barChart as form barChart.png in curr directory
    f_output  = os.path.join(__dirpath__, './barChart.png')

    barChart(art_avg,f_output)

if __name__ == "__main__":
    main()
