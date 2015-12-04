import re

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
def get_sentiment_score(status):
    statusString = TextBlob(status)
    sentiment = statusString.sentiment
    sentimentPolarityResult = statusString.sentiment.polarity
    sentimentSubjectivityResult = statusString.sentiment.subjectivity
    sentimentPolarityResult = (sentimentPolarityResult + 1.0) / 2
    return sentimentPolarityResult

init_concreteness_values()
