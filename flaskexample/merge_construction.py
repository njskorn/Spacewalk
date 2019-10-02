import geopandas as gpd
import polyline
from shapely.geometry import Point, Polygon, LineString
from flaskexample.polyline_to_df import polyline_to_df

def merge_construction(poly_route, construction_data):
    '''
    merge with construction data

    poly_route: df of google maps API directions after get_polyline
    construciton_data: imported shp file, crs fixed
    '''
    for index in range(len(poly_route)):
        line = gpd.GeoDataFrame()
        line.loc[index,'geometry']=poly_route.loc[index]['geometry']
        line.crs = {'init' :'epsg:4326'}
        line.to_crs = {'init' :'epsg:4326'}

        merger = gpd.sjoin(line, construction_data, how="left", op='intersects')
        poly_route.loc[index]['Construction'] = merger['permit_typ'].unique()
        poly_route.loc[index]['PCI_Score'] = merger['PCI_Score'].min()
        poly_route.loc[index]['Accepted_For_Maintenance'] = merger['Street_Acc'].min()
        poly_route.loc[index]['class'] = merger['class'].min()
        poly_route.loc[index]['curbrampwo'] = merger['curbrampwo'].min()
        poly_route.loc[index]['width_min'] = merger['width_min'].min()
        poly_route.loc[index]['width_reco'] = merger['width_reco'].min()
        poly_route.loc[index]['status'] = merger['status'].min()
        poly_route.loc[index]['permit_zip'] = merger['permit_zip'].max()

    return poly_route
