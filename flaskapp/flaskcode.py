from flask import Flask, render_template, request, make_response
import json
from flask.json import jsonify
from flaskext.mysql import MySQL
from _mysql_exceptions import IntegrityError
import requests
import pymongo
from pymongo import MongoClient
import pickle
import nltk
from nltk.tokenize import sent_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import BigramAssocMeasures
from nltk import pos_tag
import re

app = Flask(__name__)

client=MongoClient('localhost', 27017)
db = client["6339project"] #db name
col=db["restaurant_menu"] #collection name
not_found=db["not_found"] #collection name
menu_items=db["extracted_menu_items"] #collection name
mongo_review = db["reviews"]
items_found_info = db['food_items_found1']
items_found_sent = db['food_items_found_sent']

print "reading pickle file started"
f = open('my_classifier.pickle')
classifier = pickle.load(f)
f.close()
print "done with reading pickle file started"

def word_feats(words):
    features = dict([(word, True) for word in words])

    finder = BigramCollocationFinder.from_words(words)
    finder.apply_word_filter(lambda x: False if re.match('\w', x) else True)
    bigrams = finder.nbest(BigramAssocMeasures.chi_sq, 20000)
    features.update(dict([(bigram, True) for bigram in bigrams]))

    return features

def tokenize(sentence):
    tokens = word_tokenize(sentence.lower())
    return [w for w in tokens if not w in stopwords.words('english')]

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route('/search',methods=['POST'])  
def  search():
    '''
    Get the drugnam given in the html form.
    '''
    restaurant_name = request.form['name']
    
    category = request.form['category']
    
    city = request.form['city']
    
    global JSON_RESULT
    '''
    Return the final attached result to display on the html page.
    '''
    return (jsonify(Result = JSON_RESULT))
 
def fetchone_dict(cursor):
    data = cursor.fetchone()

    if data == None:
        return

    desc = cursor.description
    #print desc
    
    d = {}
    for i in range(len(desc)):
        d[desc[i][0]] = data[i]

    return d

"""
create table business (b_id varchar(50) PRIMARY KEY, b_name varchar(250) NOT NULL, b_address varchar(500), 
b_review_count int, b_long float(10,6), b_lat float(10,6), b_categofies varchar(250), 
b_city varchar(10), b_stars int, b_attributes blob, b_type varchar(50));
{"business_id": "vcNAWiLM4dR7D2nwwJ7nCA", "full_address": "4840 E Indian School Rd\nSte 101\nPhoenix, AZ 85018", "hours": {"Tuesday": {"close": "17:00", "open": "08:00"}, "Friday": {"close": "17:00", "open": "08:00"}, "Monday": {"close": "17:00", "open": "08:00"}, "Wednesday": {"close": "17:00", "open": "08:00"}, "Thursday": {"close": "17:00", "open": "08:00"}}, "open": True, "categories": ["Doctors", "Health & Medical"], "city": "Phoenix", "review_count": 9, "name": "Eric Goldberg, MD", "neighborhoods": [], "longitude": -111.98375799999999, "state": "AZ", "stars": 3.5, "latitude": 33.499313000000001, "attributes": {"By Appointment Only": True}, "type": "business"}
"""
def populate_business_table(file_path):
    f = open(file_path, 'r')

    connection = mysql.connect()
    for line in f:
        line = eval(line)
        b_id = line['business_id']
        b_name = line['name']

        cursor = connection.cursor()
        query = """INSERT INTO business values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""" 
        try:
            cursor.execute(query, (line['business_id'], line['name'], line['full_address'],\
                    line['review_count'], line['longitude'], line['latitude'], ",".join(line['categories']),\
                    line['city'], line['stars'], json.dumps(line['attributes']), line['type']))
        except IntegrityError:
            continue
    connection.commit()
    return

"""
/*{"votes": {"funny": 0, "useful": 2, "cool": 1}, "user_id": "Xqd0DzHaiyRqVH3WRG7hzg", "review_id": "15SdjuK7DmYqUAj6rjGowg", "stars": 5, "predicted_sentiment": "neg", "date": "2007-05-17", "text": "dr. goldberg offers everything i look for in a general practitioner.  he's nice and easy to talk to without being patronizing; he's always on time in seeing his patients; he's affiliated with a top-notch hospital (nyu) which my parents have explained to me is very important in case something happens and you need surgery; and you can get referrals to see specialists without having to see him first.  really, what more do you need?  i'm sitting here trying to think of any complaints i have about him, but i'm really drawing a blank.", "type": "review", "business_id": "vcNAWiLM4dR7D2nwwJ7nCA"} */

create table reviews(r_id varchar(50) PRIMARY KEY, r_user_id varchar(50) NOT NULL, r_stars int, r_predicted_sentiment varchar(10), r_date date, r_text blob, r_type varchar(50), r_business_id varchar(50), FOREIGN KEY(r_business_id) REFERENCES business(b_id));
"""
def populate_review_table(file_path):
    print 'here'
    f = open(file_path, 'r')

    connection = mysql.connect()
    for line in f:
        line = eval(line)

        cursor = connection.cursor()
        query = """INSERT INTO reviews values(%s, %s, %s, %s, %s, %s, %s, %s)""" 
        try:
            data = (line['review_id'], line['user_id'], line['stars'], line['predicted_sentiment'], line['date'], line['text'], line['type'], line['business_id'])
        except KeyError:
            print line
            exit()
        try:
            cursor.execute(query, data)
        except IntegrityError:
            print 'IntegrityError'
            continue
    connection.commit()
    return

def populate_review_mongo(file_path):
    print 'here'
    f = open(file_path, 'r')

    for line in f:
        line = eval(line)
        mongo_review.insert(line)  
    return

@app.route('/top_food', methods=['GET'])
def get_top_food_items():
    restaurant_name = request.args.get('restaurant_name')
    return jsonify()

@app.route('/review_rating', methods=['GET'])
def get_review_rating_history():
    restaurant_name = request.args.get('restaurant_name')
    connection = mysql.connect()
    query = """select * from reviews r, business b where r.r_business_id=b.b_id and b.b_name=%s order by r.r_date;"""
    print query, restaurant_name
    cursor = connection.cursor()
    
    cursor.execute(query, (restaurant_name, ))

    final_res = {}
    data = fetchone_dict(cursor) 
    while data != None:
        new_pos_count = new_neg_count = 0
        if data['r_predicted_sentiment'] == 'pos':
            new_pos_count = 1
        else:
            new_neg_count = 1

        try:
            pos_count, neg_count = final_res[data['r_date']]
        except KeyError:
            pos_count = neg_count = 0

        final_res[data['r_date']] = (pos_count+new_pos_count, neg_count+new_neg_count) 
        data = fetchone_dict(cursor) 

    data = sorted(final_res.items(), key=lambda x: x[0])

    csv = """"REVIEW_DATE","POS_COUNT","NEG_COUNT"\n"""
    for d in data:
        csv += str(d[0]) +","+ str(d[1][0]) + "," + str(d[1][1]) + "\n"

    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=review_stats.csv"
    return response

def get_resturant_menu():
    connection = mysql.connect()
    #query = """select * from business b where b.b_categofies like "%estaurant%";"""
    query = """select b.b_id, b.b_lat, b.b_long, b.b_name, b.b_city, count(*) as rev from reviews r, business b where b.b_id = r.r_business_id and b.b_categofies like "%estaurant%" group by r_business_id order by rev desc;"""
    cursor = connection.cursor()
    
    cursor.execute(query)
    url = "https://api.locu.com/v2/venue/search"
    data = fetchone_dict(cursor)
    f = open('menu_res.out', 'w')
    while data != None:
        print data['b_id']

        client = col.find({'searched_b_id': data['b_id']})
        if client.count() != 0:
            data = fetchone_dict(cursor)
            continue

        client1 = not_found.find({'searched_b_id': data['b_id']})
        if client.count() != 0:
            data = fetchone_dict(cursor)
            continue
        json_data = {
                        #"api_key" : "f165c0e560d0700288c2f70cf6b26e0c2de0348f",
                        "api_key": "15126fede2524c8cf66ed436662a38f75af62bc1",
                        "fields" : [ "locu_id", "name", "location", "contact", "menus" ],
                        "venue_queries" : [
                            {
                                "location" : {
                                    "locality": "Las Vegas",
                                    "geo" : {
                                        "$in_lat_lng_radius" : [-37.7750, 122.4183, 15000]
                                    }
                                },
                                "name" : "Treasure Island"
                            }
                        ]
                }
        json_data['venue_queries'][0]['location']['locality'] = data['b_city']
        json_data['venue_queries'][0]['name'] = data['b_name']
        json_data['venue_queries'][0]['location']['geo']['$in_lat_lng_radius'][0] = data['b_lat']
        json_data['venue_queries'][0]['location']['geo']['$in_lat_lng_radius'][1] = data['b_long']

        r = requests.post(url, data=json.dumps(json_data))
        
        json_res = r.json()
        json_res['searched_b_name'] = data['b_name']
        json_res['searched_b_city'] = data['b_city']
        json_res['searched_b_id'] = data['b_id']
        json_res['searched_b_long'] = data['b_long']
        json_res['searched_b_lat'] = data['b_lat']

        f.write(json.dumps(json_res)+"\n")
        if "venues" in json_res:
            if len(json_res["venues"]) > 0:
                col.insert(json_res)
            else:
                not_found.insert(json_res)
        
        data = fetchone_dict(cursor)

    f.close()

def populate_menu_items():
    client = col.find()
    data_len = client.count()
    import pdb
    #pdb.set_trace()
    for i in range(data_len):
        data = client.next()
        print data['searched_b_id'] 
        client1 = menu_items.find({'b_id': data['searched_b_id']})
        if client1.count() == 1:
            continue
        all_menu_items = []
        if len(data['venues']) == 1:
            restaurant = data['venues'][0]
            try:
                for menu in restaurant['menus']:
                    for section in menu['sections']:
                        for subsection in section['subsections']:
                            for content in subsection['contents']:
                                all_menu_items.append(content['name'])  
            except KeyError:
                continue
        else:
            print "skipping because count is not 1"
        if len(all_menu_items):
            new_items = {'menu_items': all_menu_items, 'menu_length': len(all_menu_items), 'b_name': data['searched_b_name']\
                , 'b_id': data['searched_b_id'], 'b_city': data['searched_b_city'], 'b_lat': data['searched_b_lat'], 'b_long': data['searched_b_long']}
            menu_items.insert(new_items)

def get_food_count_by_b_id():
    client = menu_items.find()
    for i in range(client.count()):
        data = client.next()
        already_done = items_found_info.find({'b_id': data['b_id']})
        if already_done.count():
            continue
        print data['b_id']
        food_items = data['menu_items']
        client1 = mongo_review.find({'business_id': data['b_id']})
        num_reviews = client1.count()
        num_items_found = 0
        items_found = {}
        for j in range(num_reviews):
            d = client1.next()
            review_text = d['text']
            for food_item in food_items:
                if food_item.lower() in review_text.lower():
                    num_items_found += 1
                    food_item = food_item.replace('.', '_')
                    try:
                        items_found[food_item] += 1
                    except KeyError:
                        items_found[food_item] = 1

        res = {'b_id': data['b_id'], 'num_reviews': num_reviews, 'num_items_found': num_items_found, 'num_food_items': len(food_items), 'items_found': items_found}
        items_found_info.insert(res)

def predict_food_sentiment():
    client = items_found_info.find().sort("num_items_found", pymongo.DESCENDING)
    for i in xrange(client.count()):
        data = client.next()
        client2 = items_found_sent.find({'b_id': data['b_id']})
        if client2.count():
            continue

        client1 = mongo_review.find({'business_id': data['b_id']})
        food_items = data['items_found']
        num_reviews = client1.count()
        num_items_found_sent = 0
        items_found = {}
        for j in range(num_reviews):
            d = client1.next()
            review_text = d['text']
            sentences = sent_tokenize(review_text)
            for sentence in sentences:
                for food_item in food_items:
                    food_item = food_item.replace('_', '.')
                    if food_item.lower() in sentence.lower():
                        output_class = classifier.classify(word_feats(tokenize(sentence)))
                        print output_class
                        num_items_found_sent += 1
                        food_item = food_item.replace('.', '_')
                        try:
                            current_count = items_found[food_item]
                        except KeyError:
                            current_count = {'pos': 0, 'neg': 0, 'pos_sentences': [], 'neg_sentences': []}
                            items_found[food_item] = current_count

                        items_found[food_item][output_class] += 1
                        if output_class == 'pos':
                            items_found[food_item]['pos_sentences'].append(sentence)
                        else:
                            items_found[food_item]['neg_sentences'].append(sentence)

        res = {'items_found_sent': items_found, 'b_id': data['b_id'], 'num_items_found_sent': num_items_found_sent}
        items_found_sent.insert(res)

JSON_RESULT = []
if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()

    mysql = MySQL()

    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    app.config['MYSQL_DATABASE_DB'] = '6339project'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'

    mysql.init_app(app)

    #get_resturant_menu()

    #populate_business_table('business.json')
    #populate_review_table('review_sent.json')

    #populate_review_mongo('review_sent.json')

    #populate_menu_items()
    #get_food_count_by_b_id()

    predict_food_sentiment()
    #print get_review_rating_history('Treasure Island, LLC')

    app.debug = True
    app.run(debug=True)
