import json
import operator

def getCCData(city, category):
    busOperation={}
    def getCheckinData():
        with open('E:\\Study\\yelp_dataset_challenge_academic_dataset\\yelp_academic_dataset_checkin.json') as f:
        #with open('C:\\Users\\Pawan\\Desktop\\testbusiness.json') as f:
            for line in f:
                data = json.loads(line)
                busOperation[data['business_id']] = {'totalcheckin' : sum(data['checkin_info'].values())}
                
    businessData={}
    categories=[]
    getBestBusCity={}
    
    
        
    def getBusinessData():
        with open('E:\\Study\\yelp_dataset_challenge_academic_dataset\\yelp_academic_dataset_business.json') as f:
        #with open('C:\\Users\\Pawan\\Desktop\\testbusiness.json') as f:
            for line in f:
                data = json.loads(line)
                
                #categories = data['categories']
                #categories = categories + list(set(data['categories']) - set(categories))
                #Get all the records with category Restaurants 
                #if('Restaurants' in categories):
                '''if (data['business_id'] in businessData):
                    stars = businessData[data['business_id']]['rating'] + data['stars']
                    if(data['business_id'] in busOperation):
                        totalcheckin = busOperation[data['business_id']]['totalcheckin'] + businessData[data['business_id']]['totalcheckin']
                    else:
                        totalcheckin = 0
                    businessData[data['business_id']].append({'address':data['full_address'], 
                                                            'categories':data['categories'], 
                                                            'city':data['city'],
                                                            'state':data['state'],
                                                            'rating': stars,
                                                            'name':data['name'],
                                                            'longitude':data['longitude'],
                                                            'latitude':data['latitude'],
                                                            'reviewcount':data['review_count'],
                                                            'totalcheckin':totalcheckin
                                                            })
                else:
                 '''
                totalcheckin = 0
                if(data['business_id'] in busOperation):
                    totalcheckin = busOperation[data['business_id']]['totalcheckin']
                    businessData[data['business_id']] = {'address':data['full_address'], 
                                                        'categories':data['categories'], 
                                                        'city':data['city'].lower(),
                                                        'state':data['state'],
                                                        'name':data['name'],
                                                        'rating': float(data['stars']),
                                                        'longitude':data['longitude'],
                                                        'latitude':data['latitude'],
                                                        'reviewcount':int(data['review_count']),
                                                        'totalcheckin':int(totalcheckin),
                                                        'attributes':data['attributes']
                                                        }
                    #rank = round(((totalcheckin +  data['stars'] + data['review_count'])/3),2)
                    if (data['city'].lower() in getBestBusCity):
                        getBestBusCity[(data['city']).lower()].append({'businessid':data['business_id'],
                                                             'categories':data['categories'],
                                                             'longitude':data['longitude'],
                                                             'latitude':data['latitude'],
                                                             'rating': float(data['stars']),
                                                             'name':data['name'],
                                                             'reviewcount':int(data['review_count']),
                                                             'totalcheckin':int(totalcheckin),
                                                             'attributes':data['attributes']})
                    else:
                        getBestBusCity[(data['city']).lower()] = [{'businessid':data['business_id'],
                                                         'categories':data['categories'],
                                                         'longitude':data['longitude'],
                                                         'latitude':data['latitude'],
                                                         'rating': float(data['stars']),
                                                         'name':data['name'],
                                                         'reviewcount':int(data['review_count']),
                                                         'totalcheckin':int(totalcheckin),
                                                         'attributes':data['attributes']}]
                else:
                    businessData[data['business_id']] = {'address':data['full_address'], 
                                                        'categories':data['categories'], 
                                                        'city':data['city'].lower(),
                                                        'state':data['state'],
                                                        'name':data['name'],
                                                        'rating': float(data['stars']),
                                                        'longitude':data['longitude'],
                                                        'latitude':data['latitude'],
                                                        'reviewcount':int(data['review_count']),
                                                        'totalcheckin':int(totalcheckin),
                                                        'attributes':data['attributes']
                                                        }
                    #rank = round(((totalcheckin +  data['stars'] + data['review_count'])/3),2)
                    if (data['city'].lower() in getBestBusCity):
                        getBestBusCity[data['city'].lower()].append({'businessid':data['business_id'],
                                                             'categories':data['categories'],
                                                             'longitude':data['longitude'],
                                                             'latitude':data['latitude'],
                                                             'rating': float(data['stars']),
                                                             'name':data['name'],
                                                             'reviewcount':int(data['review_count']),
                                                             'totalcheckin':int(totalcheckin),
                                                             'attributes':data['attributes']})
        #'rank' : rank})
                    else:
                        getBestBusCity[data['city'].lower()] = [{'businessid':data['business_id'],
                                                         'categories':data['categories'],
                                                         'longitude':data['longitude'],
                                                         'latitude':data['latitude'],
                                                         'rating': float(data['stars']),
                                                         'name':data['name'],
                                                         'reviewcount':int(data['review_count']),
                                                         'totalcheckin':int(totalcheckin),
                                                         'attributes':data['attributes']}]
    #'rank' : rank}]
    getRec = []
    def allData():
        getCheckinData()
        getBusinessData()
    
        cityData = getBestBusCity[city.lower()]
    
        '''
        averageLat=0.0
        averageLon=0.0
        latloncount = 0
        '''
        
        for citydata in cityData:
            cityCategory = [x.lower() for x in citydata['categories']]
            if (category.lower() in cityCategory):
        #        averageLat = averageLat + citydata['latitude']
        #        averageLon = averageLon + citydata['longitude']
        #        latloncount = latloncount + 1
                getRec.append(citydata)
    #print len(getRec)
    #nextSkyline= set()
    allData()
    firstBusines = None
    # function to get the skyline data
    def getTopBusiness(allBusData):
        firstBusines = {}
        nextSkyline = set()
        if len(allBusData) >= 5:
            for firstBusines in allBusData:
                for businessrec in allBusData:
                    if firstBusines['businessid'] == businessrec['businessid']:
                        continue
                    if businessrec['reviewcount'] >= firstBusines['reviewcount'] and businessrec['rating'] >= firstBusines['rating'] and businessrec['totalcheckin'] >= firstBusines['totalcheckin']:
                        nextSkyline.add(firstBusines['businessid'])
                    elif businessrec['reviewcount'] <= firstBusines['reviewcount'] and businessrec['rating'] <= firstBusines['rating'] and businessrec['totalcheckin'] <= firstBusines['totalcheckin']:
                        nextSkyline.add(businessrec['businessid'])
        else:
            return allBusData,nextSkyline 
        
        temp = [x['businessid'] for x in allBusData]
        temp1 = list(set(temp) - set(nextSkyline))
        #print len(temp1)
        final_res = []
        for t in allBusData:
            if t['businessid'] in temp1:
                final_res.append(t)
        return final_res,nextSkyline                 
    
    skyBusiness,nextSkyBus = getTopBusiness(getRec)
    #print len(skyBusiness)
    #for sky in skyBusiness:
        #print sky['rating'],sky['reviewcount'],sky['totalcheckin']
    
    #print len(skyBusiness),len(nextSkyBus) 
    
    def getTop100NextSky():
        top100NextSkyline = []
        allNextSkyData = nextSkyBus
        nextSkyIter = getBusIDData(allNextSkyData)
        required_count = max(int((len(getRec)*20)/100), 100)
        if len(nextSkyBus) > required_count:
            while (len(top100NextSkyline) < required_count):
                #print len(nextSkyIter)
                topNextSkyline,allNextSkyData = getTopBusiness(nextSkyIter)
                for skyData in topNextSkyline:
                    top100NextSkyline.append(skyData)
            return top100NextSkyline
        else:
            return getBusIDData(nextSkyBus)
    
    def getBusIDData(setOfBusinessIds):
        setBusinessData = []
        for t in getRec:
            if t['businessid'] in setOfBusinessIds:
                setBusinessData.append(t)
        return setBusinessData
    
    def getBusAttributes():
        topNextSkyData = getTop100NextSky()
        for bus in skyBusiness:
            topNextSkyData.append(bus)
    #    print len(topNextSkyData)
        # for next 100 skydata get the attributes
        attributes_count = {}
        for skyData in topNextSkyData:
            allAttributes = skyData['attributes']
            for key,val in allAttributes.iteritems():
                if type(val) is dict:
                    for key1,val1 in val.iteritems():
                        att = (key1, val1)
                        if att in attributes_count:
                            prevCount = attributes_count[att]
                            attributes_count [att] = 1 + prevCount
                        else:
                            attributes_count [att] = 1
                else:
                    att = (key, val)
                    if att in attributes_count:
                        prevCount = attributes_count[att]
                        attributes_count [att] = 1 + prevCount
                    else:
                        attributes_count [att] = 1
        return attributes_count
    
    def finalAttributes():
        att_count = getBusAttributes()
        falseatt = {}
        trueatt = {}
        others = {}
        final_att = {}
        for att in att_count:
            if att[1] == False:
                if att_count[att] > 0:
                    falseatt[att[0]]=att_count[att]
            elif att[1] == True:
                if att_count[att] > 0:
                    trueatt[att[0]]=att_count[att]
            else:
                if att_count[att] > 0:
                    others[att[0]]=att_count[att]
        
        #final_att['true'] = trueatt
        final_att['true'] = dict(sorted(trueatt.iteritems(), key=operator.itemgetter(1), reverse=True)[:6])
        #final_att['false'] = falseatt
        final_att['false'] = dict(sorted(falseatt.iteritems(), key=operator.itemgetter(1), reverse=True)[:6])
        #final_att['others'] = others
        final_att['others'] = dict(sorted(others.iteritems(), key=operator.itemgetter(1), reverse=True)[:6])
        
        return final_att,skyBusiness
    
    return finalAttributes()    
    #averageLat = averageLat/latloncount
    #averageLon = averageLon/latloncount
    
    # divide the data into north south and eash west
    # x = x is longitude (East/West), and y is latitude
    '''
    for rec in getRec:
        if rec['latitude'] > averageLat:
            print averageLat
    
    print averageLat 
    print averageLon
    '''
    #print getRec          
    #top5Rec = sorted(getRec, key=lambda k: k['rank'], reverse=True)[:5]
    #print top5Rec
    
    ''' 
    # Get details from business review file           
    businessReview={}
    with open('E:\\Study\\yelp_dataset_challenge_academic_dataset\\yelp_academic_dataset_review.json') as f:
        for line in f:
            data = json.loads(line)
            if (data['business_id'] in businessReview):
                businessReview[data['business_id']].append({'review':data['text'], 'date':data['date'], 'rating':data['stars']})
            else:
                businessReview[data['business_id']] = [{'review':data['text'], 'date':data['date'], 'rating':data['stars']}]
    print len(businessReview)
    print len(businessReview['4bEjOyTaDG24SY5TxsaUNQ'])
    '''        
    
#print getCCData("charlotte","Restaurants")    