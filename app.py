from flask import Flask, request, render_template
import requests
from flask_cors import CORS
import json
import os
# from flask_pymongo import PyMongo
# from pymongo import MongoClient
from forest import findAcc
# from apscheduler.scheduler import Scheduler

app = Flask(__name__)
mapboxToken = os.getenv('MAPBOX_TOKEN')

# CORS
CORS(app)

# to be watched coords
coords = []

# # Initialized scheduler
# cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
# cron.start()
# @cron.interval_schedule(seconds=20)
# def job_function():
#     for lat, lng, name in coords:
#         updateData(lat, lng, name)


def updateData(lat, lng, location):
    name = lat + lng
    URL = 'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/' + lng + ',' + lat + ',15/800x600?access_token=' + mapboxToken
    r = requests.get(url = URL, stream =True)
    if r.status_code == 200:
        with open("/static/Images/" + name + '.png', 'wb') as f:
            f.write(r.content)
    findAcc('/static/Images/' + name + '.png', name)

@app.route('/')
def hello_world():
    return render_template('index2.html')

@app.route('/getpaths', methods=['GET'])
def getpaths():
    paths = [] # mongo.db.images.find({})
    results = []
    for res in paths:
        results.append([res['path'], res['name']])
        coords.append((res['lat'], res['lng'], res['name']))
    return json.dumps(results)
    
 
@app.route('/addnew', methods=['GET'])
def addnew():
    coord = (request.args.get('lat'), request.args.get('lng'), request.args.get('name'))
    coords.append(coord)
    updateData(coord[0], coord[1], request.args.get('name'))
    return '200'