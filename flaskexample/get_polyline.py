import geopandas as gpd
import polyline
from shapely.geometry import Point, Polygon, LineString
from flaskexample.polyline_to_df import polyline_to_df

def get_polyline(routes, my_route):
    '''
    get polylines

    routes: json route dict from google maps API
    my_route: index of current route
    '''
    poly_route = gpd.GeoDataFrame()
    poly_route['geometry'] = None

    for i in range(len(routes[my_route]['legs'][0]['steps'])):
        shape = routes[my_route]['legs'][0]['steps'][i]['polyline']['points']
        poly_route = polyline_to_df(poly_route, shape, i)

        poly_route.crs = {'init' :'epsg:4326'}
        poly_route.to_crs = {'init' :'epsg:4326'}

    poly_route['Construction'] = None
    poly_route['PCI_Score'] = None
    poly_route['width_min'] = None
    poly_route['Accepted_For_Maintenance'] = None
    poly_route['class'] = None
    poly_route['curbrampwo'] = None
    poly_route['width_reco'] = None
    poly_route['status'] = None
    poly_route['permit_zip'] = None

    return poly_route
