import sys
import os
import dstats
import songprofiling
import argparse
from dstats import token_words
from songprofiling import term_occurance
def process(songdata,song_id1,song_id2):
    #make id2 comes later than id1 just for simplicity
    song_id1,song_id2 = fix(song_id1,song_id2)
    #dictionaries for words in lyric
    dict1 = defaultdict(int)
    dict2 = defaultdict(int)
    csv_songdata = csv.DictReader(songdata)
    counter = 0
    for row in csv_songdata:
        counter += 1
        if counter == song_id1:
            dict1 = term_occurnace(token_words(row['text']))
        if counter == song_id2:
            dict2 = term_occurance(token_words(row['text']))
            break;
    return jaccard(dict1,dict2);
def fix(a,b):
    if a > b:
        temp  = a
        a = b
        b = temp
    return a,b
def jaccard(song1,song2):
#in: dictionary of song1, song2
#return : float value equal to intersect(song1,song2) / union(song1,song2)
    value   = 0
    num = intersect(song1,song2)
    denom = union(song1,song2)
    return num/denom
def intersect(song1,song2):
    sum = 0
    for key in song1:
        if key in song2.keys():
            sum += 1
    return sum
def union(song1,song2):
    sum = len(song1)
    for key in song2:
        if key not in song1.keys():
            sum += 1
    return sum
def main():
    parser = argparse.ArgumentParser(description = 'Takes songdata(in csv), and 2 song_id then print jaccard value of the 2 song')
    parser.add_argument('--songdata',action="store",type = FileType(mode = 'r',encoding = 'UTF-8'), help = 'csvfile that has format {"artist","song(title)","link","text"}')
    parser.add_argument('--song_id1',action="store",type = int, help = 'song_id : Integer n representing nth song in the data')
    parser.add_argument('--song_id2',action="store",type = int, help = 'song_id : Integer n representing nth song in the data')
    parser.set_defaults(func = process)
    args = parser.parse_args()
    print(args)
if __name__ == "__main__":
    main()
