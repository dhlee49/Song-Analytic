#token_words to process lyric and unique_set
#to filter redundant words when counting for doc_occurance
from dstats import token_words, unique_set
#sys for sys.in
import sys
#math for idf calculation
import math
from pprint import pprint
#csv to read the sys.in csvfile
import csv
#defaultdict to organize data
from collections import defaultdict

def term_occurance(n_lyric):
#in: lyric - list of processed(regexp/stopword) words in row[text]
#return dictionary term : term occurance
    n_to = defaultdict(int)
    for term in n_lyric:
        n_to[term] += 1
    return n_to
def doc_occurance(n_lyric, doc_occ):
#in: lyric - list of processed(regexp/stopword) words in row[text]
#return modified doc_freq
    unique_lyric = unique_set(n_lyric)
    for term in unique_lyric:
        doc_occ[term] += 1
    return doc_occ
def to_and_do(csvfile):
#in: csvfile from csvDictReader
#return list of term_occurance in lyric, term_occurance in doc
    n_t_o = []
    n_d_o = defaultdict(int)
    for row in csvfile:
        #process input lyric('text') into list of words without stopwords/puncutations
        lyric = token_words(row['text'])
        n_t_o.append(term_occurance(lyric))
        doc_occurance(lyric,n_d_o)
    return n_t_o,n_d_o
def tf_idf(t_o,d_o,size):
#in: term occurance in lyric, term_occurance in doc, size of entire document
#
    word_score = defaultdict(int)
    for k in t_o:
        #Limited precision to 5 digits after decimal point
        #The calculation of idf was obtained from tutorial slide
        #which is slightly different from Sci-kit calculation of log10 of (1+n / 1+ doc_occurnace)
        word_score[k] = round((1+ math.log10(t_o[k])) * math.log10(size/d_o[k]),5)

    #sort top 50 or less(if there arent 50) important words in word socre
    if(len(word_score) < 50):
        result =  sorted(word_score.items(),key = lambda x : x[1], reverse = True)
    else :
        result = sorted(word_score.items(),key = lambda x : x[1], reverse = True)[:50]
    pprint(result)
    return
def main():
    song_data = csv.DictReader(sys.stdin)
    t_o,d_o = to_and_do(song_data)
    #iterate over list of word_occurance dictionary
    for ele in t_o:
        tf_idf(ele,d_o,len(t_o))
if __name__ == "__main__":
    main()
