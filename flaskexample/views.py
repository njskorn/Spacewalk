from flask import Flask, render_template, request
from flaskexample import app
import numpy as np
import geopandas as gpd
import polyline
from shapely.geometry import Point, Polygon, LineString
import requests
import urllib.request
import json
import csv
import time
import datetime
import re
import folium
import pickle
from flaskexample.key import my_key
import math
import os
from flaskexample.human_to_APIinput import human_to_APIinput
from flaskexample.get_polyline import get_polyline
from flaskexample.merge_construction import merge_construction
from flaskexample.pretty_construction import pretty_construction
from flaskexample.remove_tags import remove_tags
from flaskexample.polyline_to_df import polyline_to_df
from flaskexample.prep_for_xgb import prep_for_xgb
from flaskexample.xgb_helper import xgb_helper
from flaskexample.predict_width import predict_width
from flaskexample.accessibility_score import accessibility_score
from flaskexample.route_map import route_map

endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = my_key

@app.route('/')
@app.route('/index')
def index():
    return render_template('master.html')


@app.route('/go')
def go():
    # request and format API input
    origin = human_to_APIinput(request.args.get('origin'))
    destination = human_to_APIinput(request.args.get('destination'))

    # request to the API
    nav_request = 'origin={}&destination={}&key={}&mode={}&alternatives=true'.format(origin, destination, api_key,'walking')
    my_request = endpoint + nav_request
    response = urllib.request.urlopen(my_request).read()
    directions = json.loads(response)
    routes=directions['routes']

    #  import construction data
    data = gpd.read_file('SF_permit_data.shp')
    data.crs = {'init' :'epsg:4326'}
    data.to_crs({'init': 'epsg:4326'})
    data.head()

    # load the xgb model from disk
    filename = 'finalized_xgb.sav'
    xgb_model = pickle.load(open(filename, 'rb'))
    if os.path.exists("templates/new_map.html"):
        os.remove("templates/new_map.html")

    # retrieve accessibility score from each route
    score = []
    for current_route in range(len(routes)):
        # get polylines
        poly_route = get_polyline(routes,current_route)
        # merge with construction data
        poly_route = merge_construction(poly_route, data)

        # predict usable sidewalk width meets ADA required 5 ft
        route_to_xgb = poly_route.copy()
        ready_route = prep_for_xgb(route_to_xgb)
        poly_route['route_width_preds'] = xgb_helper(xgb_model, ready_route)

        # accessibility score
        score.append(accessibility_score(poly_route))

    best_route = np.argmax(score)

    poly_route = get_polyline(routes,best_route)
    poly_route = merge_construction(poly_route, data)
    route_to_xgb = poly_route.copy()
    ready_route = prep_for_xgb(route_to_xgb)
    poly_route['route_width_preds'] = xgb_helper(xgb_model, ready_route)

    # HTML Instructions for each step
    output = [None]*len(routes[best_route]['legs'][0]['steps'])
    for i in range(len(routes[best_route]['legs'][0]['steps'])):
        my_step = routes[best_route]['legs'][0]['steps'][i]
        plaintext = remove_tags(my_step['html_instructions'])
        output[i] = plaintext

    # merge with html_instructions
    poly_route['html']=output

    # clean up formatting for final presentation
    for index in range(len(poly_route)):
        poly_route.loc[index]['Construction'] = [x for x in poly_route.loc[index]['Construction'] if str(x) != 'nan']
    poly_route['Construction'] = poly_route['Construction'].apply(lambda y: np.nan if len(y)==0 else y)
    poly_route['Construction'].fillna('No construction', inplace=True)
    poly_route['PCI_Score'].fillna('No record', inplace=True)
    poly_route = pretty_construction(poly_route)
    poly_route['route_width_preds'] = poly_route['route_width_preds'].map({1: 'Yes', 0: 'No'})

    # render map for output page
    filename=origin+destination+'.html'
    route_map(routes,poly_route,best_route,filename)
    #poly_route = 1
    #score = [1]
    #best_route = 0
    return render_template('go.html', route_steps=poly_route, score=score[best_route], my_map_image=filename)
