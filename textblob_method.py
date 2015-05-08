from textblob import TextBlob
 
f = open('review_15000.json', 'r')

correct = 0
wrong = 0
for line in f:
    line = eval(line)
    t = TextBlob(line['text'])
    polarity = t.sentiment.polarity

    if line['stars'] >= 3.5 and polarity >= 0.3:
        correct+=1
    elif line['stars'] >= 3.5 and polarity < 0.3:
        wrong+=1
    elif line['stars'] <= 3.5 and polarity <= 0.3:
        correct+=1
    elif line['stars'] <= 3.5 and polarity > 0.3:
        wrong+=1

print correct, wrong, correct/float(correct+wrong)
