f = open('review.json', 'r')

business = {}

for line in f:
    line = eval(line)
    try:
        business[line['business_id']] += 1
    except KeyError:
        business[line['business_id']] = 1

for t in business:
    print str(t)+","+str(business[t])
