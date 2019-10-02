import numpy as np
import pandas as pd

def prep_for_xgb(route_to_RF):
    '''
    preps a dataframe for XGBoost Classifer to predict sidewalk width
    drops geometry and html columns
    one-hot encodes construction data, zip code data, and road class data
        zip and road class are drop one, construction is NOT
    resets column order for xgb classifier
    '''

    # set columns
    cat_class=['Commercial Throughway','Downtown Commercial','Downtown Residential','Mixed-use',
               'Neighborhood Commercial','Neighborhood Residential','Park Interior','Residential Throughway',]
    cat_construction = [ 'AddlStSpac','Display','ExcStreet','Excavation','MinorEnc','OverwideDr','Sidewalk',
                        'SpecSide','StreetSpace','StrtImprov','TableChair','TempOccup','Wireless','conformity',
                        'minorenc']
    cat_zips=[94103.0,94104.0,94105.0,94107.0,94108.0,94111.0,94158.0]


    route_to_RF.drop(['geometry'], axis=1, inplace=True)
    route_to_RF['permit_zip'].astype('float')

    for cat in cat_construction:
        route_to_RF[cat] = None
    for cat in cat_class:
        route_to_RF[cat] = None
    for cat in cat_zips:
        route_to_RF[cat] = None
    for index in range(len(route_to_RF)):
        for cat in cat_construction:
            route_to_RF.loc[index][cat] = (cat in route_to_RF.loc[index]['Construction'])
        for cat in cat_class:
            route_to_RF.loc[index][cat] = (cat == route_to_RF.loc[index]['class'])
        for cat in cat_zips:
            route_to_RF.loc[index][cat] = (cat == route_to_RF.loc[index]['permit_zip'])

    route_to_RF.drop(['Construction','class','permit_zip'], axis=1, inplace=True)
    route_to_RF['Accepted_For_Maintenance'] = route_to_RF['Accepted_For_Maintenance'].map({'Yes': 1, 'No': 0})
    route_to_RF['status'] = route_to_RF['status'].map({'ACTIVE': int(1), 'APPROVED': int(0)})
    route_to_RF['curbrampwo'] = route_to_RF['curbrampwo'].map({'T': 1, '?': 0})

    feat_list=['AddlStSpac','Display','ExcStreet','Excavation','MinorEnc','OverwideDr','Sidewalk','SpecSide',
               'StreetSpace','StrtImprov','TableChair','TempOccup','Wireless','conformity','minorenc',
               'Commercial Throughway','Downtown Commercial','Downtown Residential','Mixed-use',
               'Neighborhood Commercial','Neighborhood Residential','Park Interior',
               'Residential Throughway',94103.0,94104.0,94105.0,94107.0,94108.0,94111.0,94158.0]
    for feat in feat_list:
        route_to_RF[feat] = route_to_RF[feat].map({True: 1.0, False: 0.0})

    col_order = ['width_min','width_reco','PCI_Score','Accepted_For_Maintenance','curbrampwo','status','AddlStSpac',
                 'Display','ExcStreet','Excavation','MinorEnc','OverwideDr','Sidewalk','SpecSide','StreetSpace',
                 'StrtImprov','TableChair','TempOccup','Wireless','conformity','minorenc','Commercial Throughway',
                 'Downtown Commercial','Downtown Residential','Mixed-use','Neighborhood Commercial',
                 'Neighborhood Residential','Park Interior','Residential Throughway',94103.0,94104.0,94105.0,
                 94107.0,94108.0,94111.0,94158.0]

    route_to_RF = route_to_RF[col_order]
    route_to_RF['PCI_Score'] = route_to_RF['PCI_Score'].astype(np.float64)
    route_to_RF['curbrampwo'] = route_to_RF['curbrampwo'].astype(np.float64)
    route_to_RF['Accepted_For_Maintenance'] = route_to_RF['Accepted_For_Maintenance'].astype(np.float64)
    route_to_RF['status'] = route_to_RF['status'].astype(np.float64)


    return route_to_RF
