import numpy as np
import geopandas as gdp

def accessibility_score(gdf):
    '''
    Current overall accessibility metric
    *future* customize based on custom user importance

    Curb: Percentage of construction not involving changes to the curb

    Pavement: Minimum pavement quality
        Changed from average based on walking the streets

    Width: Percentage of sidewalks meeting estimated minimum width requriement
    '''

    print(gdf.columns)
    # curb ramp work
    if gdf['curbrampwo'].max() == 0:
        curb = 1
    else:
        curb = 1-(sum(list(gdf['curbrampwo'].astype(int)))/len(gdf))

    # pavement quality
    pavement = np.nanmin(gdf['PCI_Score'])/100

    # sidewalk minimum width requirements
    width = sum(gdf['route_width_preds'])/len(gdf)
    #print("curb: {}, pavement: {}, width: {}".format(curb, pavement, width))

    score=(curb+pavement+width)/3

    return score
