from textblob import TextBlob

def get_sentiment_score(text):
    text = text.encode('utf8', 'replace')
    statusString = TextBlob(text)
    sentiment = statusString.sentiment
    sentimentPolarityResult = statusString.sentiment.polarity
    sentimentSubjectivityResult = statusString.sentiment.subjectivity
    sentimentPolarityResult = (sentimentPolarityResult + 1.0) / 2
    return sentimentPolarityResult
