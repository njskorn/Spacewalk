import numpy as np
import geopandas as gdp

def accessibility_score(gdf):
    score = np.nanmin(gdf['PCI_Score'])

    return score
