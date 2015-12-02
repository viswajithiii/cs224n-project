import nltk
import getopt
import sys
import json
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
import pickle

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f:", ["filepath="])
    except getopt.GetoptError:
        print "Invalid or missing arguments"
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-f", "--filepath"):
            filePath = arg

    if filePath=='':
        print "Provide path to all files"
        sys.exit(2)
#    if filePath[-1] != '/':
#        filePath.append('/')

    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    all_sentences = []
    total_descs = 0
    with open(filePath, 'r') as project_file:
        # for each project
        i = 0
        for line in project_file:
            print i
            i += 1
#            if i > 3:
#                break
            project_data = json.loads(line)
            #print project_data["project_name"]

            ds = project_data["daily_snapshots"]
            days_list = sorted(ds, key=lambda x: int(x))
            for day_number in days_list:
#                print ds[day_number]["full_description"]
                sentences = sent_detector.tokenize(ds[day_number]["full_description"])
                all_sentences.extend(sentences)
                total_descs += 1

    print len(all_sentences)
#    print all_sentences
    count_vect = CountVectorizer(ngram_range=(1,3))
    freq_mat = count_vect.fit_transform([' '.join(all_sentences)])    
    print freq_mat.shape
#    print count_vect.vocabulary_
    pickle.dump(count_vect,open('count_vect.pkl','w'))
    print 'Number of unique tokens:', len(count_vect.vocabulary_.keys())
    print 'Total number of descriptions:', total_descs
#    print freq_mat
main()
