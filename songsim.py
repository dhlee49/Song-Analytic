#csv for csvfile process
import csv
#argparser
import argparse
from pprint import pprint
#tokenizing lyric
from dstats import token_words,unique_set
#term_occurance counter
from songprofiling import term_occurance,to_and_do,tf_idf


def process(songdata,song_id1,song_id2):
    """
    in: songcsv, song id1,2 : Integer
    return: jaccard value of song id1,2 rounded to 5 points after decimal
    """
    #make id2 comes later than id1 just for simplicity
    song_id1,song_id2 = fix(song_id1,song_id2)
    #sets for words in lyric
    set1 = {}
    set2 = {}
    counter = 0
    csv_songdata = csv.DictReader(songdata)
    list_to,d_o,n_list= to_and_do(csv_songdata)
    #list_to is list of dictinaries of words in song starting from first.
    set1 = set(tf_idf(list_to[song_id1-1],d_o,50,len(n_list)).keys())
    set2 = set(tf_idf(list_to[song_id2-1],d_o,50,len(n_list)).keys())
    return jaccard(set1,set2);
def fix(a,b):
    """
    in : 2 integer a,b
    return : a,b where a < b
    """
    if a > b:
        temp  = a
        a = b
        b = temp
    return a,b
def jaccard(set1,set2):
    """
    in: 2 sets : set1, set2
    return : float value(with prec : 5) equal to intersect(set1,set2) / union(set1,set2)
    """
    num = len(set1 & set2)
    denom = len(set1 | set2)
    return round(num/denom,10)
def main():
    parser = argparse.ArgumentParser(description = 'Takes songdata(in csv), and 2 song_id then print jaccard value of the 2 song')
    parser.add_argument("songdata",type = argparse.FileType('r'), help = 'csvfile that has format {"artist","song(title)","link","text"}')
    parser.add_argument("song_id1",type = int, help = ' song_id1 : Integer n representing nth song in the data')
    parser.add_argument("song_id2",type = int, help = ' song_id2 : Integer n representing nth song in the data')
    args = parser.parse_args()
    jac = process(args.songdata, args.song_id1,args.song_id2)
    print('Jaccard between : %d and %d is %f' % (args.song_id1,args.song_id2,jac))
if __name__ == "__main__":
    main()
