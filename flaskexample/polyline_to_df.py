import geopandas as gpd
import polyline
from shapely.geometry import Point, Polygon, LineString

def polyline_to_df(gdf,shape, i):
    decoded_shape = polyline.decode(shape,geojson=True)
    line = LineString(decoded_shape)
    std_buffer = 0.0001
    buffline = line.buffer(std_buffer)

    #my_line = gpd.GeoDataFrame()
    #my_line['geometry'] = None
    gdf.loc[i, 'geometry'] = buffline

    return gdf
