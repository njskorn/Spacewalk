import pandas as pd
from flaskexample.predict_width import predict_width

def xgb_helper(model, route):
    '''
    breaks a route into individual steps with recognizable columns
    route: df of route steps

    assumes columns are preprocessed for XGBoost with prep_for_xgb()
    '''
    preds=[]

    col_order = ['width_min','width_reco','PCI_Score','Accepted_For_Maintenance','curbrampwo','status','AddlStSpac',
                 'Display','ExcStreet','Excavation','MinorEnc','OverwideDr','Sidewalk','SpecSide','StreetSpace',
                 'StrtImprov','TableChair','TempOccup','Wireless','conformity','minorenc','Commercial Throughway',
                 'Downtown Commercial','Downtown Residential','Mixed-use','Neighborhood Commercial',
                 'Neighborhood Residential','Park Interior','Residential Throughway',94103.0,94104.0,94105.0,
                 94107.0,94108.0,94111.0,94158.0]

    for index in range(len(route)):
        my_step = pd.DataFrame(columns=col_order)
        my_step.loc[0]=route.loc[index]
        pred = int(predict_width(model, my_step))
        preds.append(pred)
    return preds
