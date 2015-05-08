import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures
from nltk import pos_tag
import random
import re
import json
import sys
import pickle
 
def word_feats(words):
    features = dict([(word, True) for word in words])

    finder = BigramCollocationFinder.from_words(words)
    finder.apply_word_filter(lambda x: False if re.match('\w', x) else True)
    bigrams = finder.nbest(BigramAssocMeasures.chi_sq, 20000)
    features.update(dict([(bigram, True) for bigram in bigrams]))

    return features
 
def tokenize(sentence):
    tokens = word_tokenize(sentence.lower())
    return [w for w in tokens if not w in stopwords.words('english')]# and re.match('\w', w)]

f = open('my_classifier.pickle', 'r')
classifier = pickle.load(f)
f.close()

f_out = open('review_sentiment_full_2.json', 'w')
f = open('review.json', 'r')
read = 0
tp = tn = fp = fn = 0
for line in f:
    line = eval(line)
    read+=1
    try:
        output_class = classifier.classify(word_feats(tokenize(line['text'])))
    except:
        print "error", read
        continue
    line['predicted_sentiment'] = output_class

    if output_class == 'pos' and line['stars'] >= 3.5:
        tp += 1
    elif output_class == 'neg' and line['stars'] >= 3.5:
        fn += 1
    elif output_class == 'pos' and line['stars'] < 3.5:
        fp += 1 
    elif output_class == 'neg' and line['stars'] < 3.5:
        tn += 1 

    f_out.write(json.dumps(line)+"\n")

    if read % 1000 == 0:
        print read

print "total",read, "tp", tp, "tn", tn, "fp", fp, "fn", fn
classifier.show_most_informative_features()
