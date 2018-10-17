#csv for csvfile process
import csv
#argparser
import argparse
from pprint import pprint
#tokenizing lyric
from dstats import token_words,unique_set
#term_occurance counter
from artistprofiling import to_and_do
from songprofiling import tf_idf
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
    t_o,d_o,size = to_and_do(csv_songdata)
    for row in t_o:
        counter += 1
        if counter == art_id1:
            set1 = set(tf_idf(t_o[row], d_o,100,size))
        if counter == art_id2:
            set2 = set(tf_idf(t_o[row], d_o,100,size))
            break
    return jaccard(set1,set2);

def main():
    parser = argparse.ArgumentParser(description = 'Takes songdata(in csv), and 2 song_id then print jaccard value of the 2 song')
    parser.add_argument("songdata",type = argparse.FileType('r'), help = 'csvfile that has format {"artist","song(title)","link","text"}')
    parser.add_argument("artist_id1",type = int, help = ' artist_id1 : Integer n representing nth artist in the data')
    parser.add_argument("artist_id2",type = int, help = ' artist_id2 : Integer n representing nth artist in the data')
    args = parser.parse_args()
    jac = process(args.songdata, args.artist_id1,args.artist_id2)
    print('jaccard value of Aritst_id1 : %d and Artist_id2 : %d is : %f' %(args.artist_id1,args.artist_id2,jac))
if __name__ == "__main__":
    main()
