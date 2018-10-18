#token_words to process lyric and unique_set
#to filter redundant words when counting for doc_occurance
from dstats import token_words, unique_set, postProcess
#sys for sys.in
import sys
#math for idf calculation
import math
from pprint import pprint
#csv to read the sys.in csvfile
import csv
#defaultdict to organize data
from collections import defaultdict,OrderedDict

def term_occurance(n_lyric):
    """
    in: lyric - list of processed(regexp/stopword) words in row[text]
    return dictionary term : term occurance
    """
    n_to = defaultdict(int)
    for term in n_lyric:
        n_to[term] += 1
    return n_to

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
    """
    in: csvfile from csvDictReader
    return list of term_occurance per song, term_occurance in doc, list of names for printing
    """
    n_t_o = []
    n_n_list = []
    n_d_o = defaultdict(int)
    for row in csvfile:
        #process input lyric('text') into list of words without stopwords/puncutations
        lyric = token_words(row['text'])
        n_n_list.append(row['song'])
        n_t_o.append(term_occurance(lyric))
        doc_occurance(lyric,n_d_o)
    return n_t_o,n_d_o,n_n_list
def tf_idf(t_o,d_o,num,size):
    """
    in: term occurance in lyric, term_occurance in doc, max number of scores showing per item, size of entire document
    prints tf_idf value of specfic song given the term occurance of the song,document occurance, and the size of entire document
    return: none
    """
    word_score = defaultdict(float)
    for k in t_o:
        #Limited precision to 5 digits after decimal point
        #The calculation of idf was obtained from tutorial slide
        #which is slightly different from Sci-kit calculation of log10 of (1+n / 1+ doc_occurnace)
        word_score[k] = round((1+ math.log10(t_o[k])) * math.log10(size/d_o[k]),5)

    #sort top 50 or less(if there arent 50) important words in word socre
    if(len(word_score) < num):
        word_score =  OrderedDict(sorted(word_score.items(),key = lambda x : x[1], reverse = True))
    else :
        word_score = OrderedDict(sorted(word_score.items(),key = lambda x : x[1], reverse = True)[:num])

    return word_score
def main():
    #csvfile in
    #sys.stdin
    #open('smalldata.csv','rU')
    song_data = csv.DictReader(sys.stdin)
    #process csvfile and generate t_o : list of dictionaries in
    t_o,d_o,n_list= to_and_do(song_data)
    list_itr = iter(n_list)
    for ele in t_o:
        print('tf_idf for song title: ', next(list_itr))
        w_s = tf_idf(ele,d_o,50,len(t_o))
        for k in w_s:
            print("{0:>13s} : {1:>8f}".format(k, w_s[k]))

if __name__ == "__main__":
    main()
