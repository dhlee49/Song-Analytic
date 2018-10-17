#token_words to process lyric and unique_set
#to filter redundant words when counting for doc_occurnace
from dstats import token_words, unique_set
#sys for sys.in
import sys
#math for idf calculation
import math
from pprint import saferepr,pprint
#csv to read the sys.in csvfile
import csv
#defaultdict to organize data
from collections import defaultdict,Counter
#songprofile for tf_idf,term_occurance, and doc_occurance function to reduce redundancy
from songprofiling import tf_idf,term_occurance

def combine_two_dict(dict_a, dict_b):
    #in two dictionaries a,b
    #return a + b
    for key in dict_b:
        if key in dict_a.keys():
            dict_a[key] += dict_b[key]
        else:
            dict_a[key] = dict_b[key]
    return dict_a
def doc_occurance(n_lyric, doc_occ):
    """
    in: lyric- set of processed(regexp/stopword) words in row[text],
    and word occurance(per row['text'])in entire document
    return modified doc_occ
    """
    unique_lyric = unique_set(n_lyric)
    for term in unique_lyric:
        doc_occ[term] += 1
    return doc_occ
def to_and_do(csvfile):
#in: csvfile from csvDictReader
#return list of term_occurance per artist, term_occurance in doc, number of artist
    n_t_o = defaultdict(defaultdict)
    n_d_o = defaultdict(int)
    size = 0
    for row in csvfile:
        size += 1
        #process input lyric('text') into list of words without stopwords/puncutations
        lyric = token_words(row['text'])
        temp = Counter(lyric)
        n_t_o[row['artist']] = combine_two_dict(n_t_o[row['artist']],temp)
    #once we establish dictionaries for all artists in collection
    #we construct our document_frequency
    for row in n_t_o:
        doc_occurance(n_t_o[row],n_d_o)
    return n_t_o,n_d_o,size

def main():
    song_data = csv.DictReader(sys.stdin)
    t_o,d_o,size = to_and_do(song_data)
    for ele in t_o:
        print("tf_idf for artist: %s" % ele)
        for item in tf_idf(t_o[ele],d_o,100,size):
            print("%s : %f " %(item,t_o[ele][item]))
if __name__ == "__main__":
    main()
