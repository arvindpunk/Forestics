from flask import Flask, request, render_template, redirect, url_for
import requests
from flask_cors import CORS
import json
import os
import hashlib
# from flask_pymongo import PyMongo
# from pymongo import MongoClient
from forest import findAcc
# from apscheduler.scheduler import Scheduler

app = Flask(__name__)
mapboxToken = os.getenv('MAPBOX_TOKEN')
baseURL = 'https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/'
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


def updateData(location):
    name = getName(location)
    print(name)
    URL = baseURL + location.lng + ',' + location.lat + ',15/800x600?access_token=' + mapboxToken
    r = requests.get(url = URL, stream = True)
    if r.status_code == 200:
        coords.append(locationObject)
        path = os.path.join('static', 'images', 'test', '.png')
        print(path)
        return
        with open(path + name + '.png', 'wb') as f:
            f.write(r.content)
        findAcc(path + name + '.png', name)
    else:
        return 'Mapbox API not responding.', 301

@app.route('/')
def home():
    return render_template('index.html')

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
    location = {
        'lat': request.args.get('lat', None),
        'lng': request.args.get('lng', None),
        'loc': request.args.get('location', None)
    }
    if isValidCoordinate(location):
        updateData(location)
        return redirect(url_for('home')), 200
    else:
        return redirect(url_for('home')), 301



# Utility
def isValidCoordinate(location):
    if location.lat and location.lng and location.loc:
        return True
    return False

def getName(location):
    locationHash = hashlib.sha256(location.lat + location.lng).hexdigest()
    return locationHash[:6] + "-" + locationHash[-6:]