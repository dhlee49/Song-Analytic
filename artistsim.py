#csv for csvfile process
import csv
#argparser
import argparse
from pprint import pprint
#tokenizing lyric
from dstats import token_words,unique_set
#term_occurance counter
from songprofiling import term_occurance
from songsim import jaccard,fix
def process(songdata,art_id1,art_id2):
    #make id2 comes later than id1 just for simplicity
    art_id1,art_id2 = fix(art_id1,art_id2)
    #sets for words in lyric
    set1 = set()
    set2 = set()
    #this program is under assumtpion that songs in csv file are grouped by artist
    #if not we can always change this to dictionary and add id to the artist in order we encounter(or any other way)
    #set for artist count(if row['artist'] not in u_art it means we are looking at next artist)
    u_art = set()
    csv_songdata = csv.DictReader(songdata)
    counter = 0
    for row in csv_songdata:
        if row['artist'] not in u_art:
            u_art.add(row['artist'])
            counter += 1
        if counter == art_id1:
            set1 = set1 | unique_set(token_words(row['text']))
        if counter == art_id2:
            set2 = set2 | unique_set(token_words(row['text']))
        #if we read everything until song_id2 no need for more
        if counter > art_id2: break

    print('union of 2 sets is :', len(set1 | set2))
    print('intersection of 2 sets is :', len(set1 & set2))
    return jaccard(set1,set2);

def main():
    parser = argparse.ArgumentParser(description = 'Takes songdata(in csv), and 2 song_id then print jaccard value of the 2 song')
    parser.add_argument("songdata",type = argparse.FileType('r'), help = 'csvfile that has format {"artist","song(title)","link","text"}')
    parser.add_argument("artist_id1",type = int, help = ' artist_id1 : Integer n representing nth artist in the data')
    parser.add_argument("artist_id2",type = int, help = ' artist_id2 : Integer n representing nth artist in the data')
    args = parser.parse_args()
    print('jaccard value is :', process(args.songdata, args.artist_id1,args.artist_id2))
if __name__ == "__main__":
    main()
