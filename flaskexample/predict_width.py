import pandas as pd
import xgboost as xgb

def predict_width(model, step):
    '''
    predict sidewalk width with previously trained XGBoost Classifier
    model: trained XGB classifier
    step: single step in route
    '''
    if step.loc[0].isnull().any():
        return 1.
    else:
        return model.predict(step)
