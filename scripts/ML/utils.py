import re
import pickle

concreteness_values = {}
def init_concreteness_values():
    with open('../../data/linguistic_data/concreteness_scores.txt', 'r') as concreteness_file:
        for line in concreteness_file:
            line = line.strip()
            line_arr = line.split(',')
            word = line_arr[0].lower()
            value = int(line_arr[1])
            value = float(value - 400) / 300.0
            concreteness_values[word] = value

liwc_dict = {}
def init_liwc_features():
    global liwc_dict
    liwc_dict = pickle.load(open('liwc_dict.pkl','r'))

def get_concreteness_score(text):
    # remove punctuations and tokenize
    words = re.findall(r'\w+', text,flags = re.UNICODE | re.LOCALE) 
    # lower case the words   
    words = map(lambda x : x.lower(), words)
    # calculate concreteness
    sum = 0.0
    count = 0
    for word in words:
        if word in concreteness_values:
            sum += concreteness_values[word]
            count += 1
    if count == 0:
        return 0.0
    else:
        return sum / count


from textblob import TextBlob
def get_sentiment_score(text):
    statusString = TextBlob(text)
    sentiment = statusString.sentiment
    sentimentPolarityResult = statusString.sentiment.polarity
    sentimentSubjectivityResult = statusString.sentiment.subjectivity
    sentimentPolarityResult = (sentimentPolarityResult + 1.0) / 2
    return sentimentPolarityResult


def search_text_in_list(liwc_list,words):
    
    count = 0
    for word in words:
        for regex_ in liwc_list:
            if regex_[-1] == '*':
                regex = '^'+regex_[:-1]
            else:
                regex = '^'+regex_+'$'
     
            match = re.search(regex,word)
            if match:
                count += 1
                break
    #                print 'Matched!',regex
    return count

def get_liwc_features(text):
    category_list = ['Posemo']
    # remove punctuations and tokenize
    words = re.findall(r'\w+', text,flags = re.UNICODE | re.LOCALE) 
    # lower case the words   
    words = map(lambda x : x.lower(), words)

    toReturn = []
    for category in category_list:
        count = search_text_in_list(liwc_dict[category],words)
        toReturn.append(count)

    return toReturn
        
init_liwc_features()
init_concreteness_values()
