f = open('review_sentiment_full_1.json', 'r')
read = 0
tp = tn = fp = fn = 0
for line in f:
    line = eval(line)
    read+=1
    output_class = line['predicted_sentiment']

    if output_class == 'pos' and line['stars'] >= 3.5:
        tp += 1
    elif output_class == 'neg' and line['stars'] >= 3.5:
        fn += 1
    elif output_class == 'pos' and line['stars'] < 3.5:
        fp += 1 
    elif output_class == 'neg' and line['stars'] < 3.5:
        tn += 1 

    if read % 1000 == 0:
        print read

print "total",read, "tp", tp, "tn", tn, "fp", fp, "fn", fn
