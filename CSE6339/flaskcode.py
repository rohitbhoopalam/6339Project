from flask import Flask, render_template, request,session
from flask_pymongo import PyMongo
from bson import json_util
import json
from flask.json import jsonify
from bson.json_util import dumps

import getRestaurants
from getRestaurants import getCCData
'''
Create an app config to store the connection details for MONGO db.
'''
app = Flask(__name__)

ATTRIBUTES = []
SKYBUSINESS = []

@app.route("/")
def home_page():
    return render_template('index.html')

@app.route('/search',methods=['GET', 'POST'])   
def  search():
    '''
    Get the drugnam given in the html form.
    '''
    restaurant_name = request.form['name']
    session['restaurant_name']=restaurant_name
    
    category = request.form['category']
    session['category']=category
    
    city = request.form['city']
    session['city']=city
    
    global ATTRIBUTES
    global SKYBUSINESS
    ATTRIBUTES,SKYBUSINESS = getCCData(city, category)
    '''
    Return the final attached result to display on the html page.
    '''
    return render_template('task3.html', attributes=ATTRIBUTES, skybusiness=SKYBUSINESS)
 
if __name__ == "__main__":
    
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run(debug=True)
