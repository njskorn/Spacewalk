import pandas as pd

pretty_dict={'TableChair':"A restaurant's table and chairs are occupying part of the sidewalk",
                     'Wireless':"Wireless cable construction",
                     'MinorEnc':"Minor sidewalk encroachment",
                     'Excavation':"Sidewalk excavation",
                     'TempOccup':"Temporary sidewalk occupation",
                     'StrtImprov':"Street improvement work",
                     'AddlStSpac':"Additional street space request",
                     'ExcStreet':"Street excavation that may encroach on the sidewalk"}

def pretty_construction(route):
    for i in range(0,len(route)):
        for index, data in enumerate(route.loc[i]['Construction']):
            for dict_key, value in pretty_dict.items():
                if pd.isnull(data):
                    route.loc[i]['Construction'][index] = 'No construction'
                elif dict_key in data:
                    route.loc[i]['Construction'][index] = data.replace(dict_key, pretty_dict[dict_key])
        route.loc[i]['Construction'] = (', '.join(list(route.loc[i]['Construction'])))
    return route
