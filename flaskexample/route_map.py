from flask import jsonify
import geopandas as gdp
import numpy as np
import pandas as pd
import polyline
from shapely.geometry import Point, Polygon, LineString
import geopandas as gpd
import folium
import os

def route_map(routes,poly_route,best,map_name):

    bounds = routes[best]['bounds']
    # set map bounds and size based on route
    mid_lat = ((bounds['northeast']['lat']+bounds['southwest']['lat'])/2)
    mid_lng = ((bounds['northeast']['lng']+bounds['southwest']['lng'])/2)
    my_map = folium.Map(location=[mid_lat, mid_lng],
               height=500,zoom_start=15)

    # Extract the point values that define the perimeter of the polygon
    for i in range(len(routes[best]['legs'][0]['steps'])):
        shape = poly_route.loc[i]['geometry']
        x, y = shape.exterior.coords.xy
        coords = np.array((y,x)).T
        #print('{}/n'.format(coords))
        folium.Polygon(coords, stroke=True, color='blue', opacity=.5,
               fillColor="blue", weight=12, fillOpacity=.9).add_to(my_map)

    output = "flaskexample/templates/"+map_name
    if os.path.exists(output):
        os.remove(output)
    my_map.save(output)
    os.chmod(output, 0o777)
