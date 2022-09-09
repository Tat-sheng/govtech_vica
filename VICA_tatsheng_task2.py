# Misc
import warnings
warnings.filterwarnings('ignore')

import json
import pandas as pd
import numpy as np


df = pd.read_csv(r'insurance_data.csv', sep = ';')
headers = df.columns.tolist()

# Change premiums to numeric
df.monthlyPremium = df.monthlyPremium.str.replace(',', '.')
df.monthlyPremium = pd.to_numeric(df.monthlyPremium , errors='coerce').fillna(0, downcast='infer')
df.totalPremium = df.totalPremium.str.replace(',', '.')
df.totalPremium = pd.to_numeric(df.totalPremium , errors='coerce').fillna(0, downcast='infer')

# Replace Misc Values
df = df.replace('Yes', True).replace('Y', True).replace('No', False).replace('N', False)
df.healthInsurance = df.healthInsurance.apply(lambda x: True if x != False else False)
df.is45OrOlder = df.is45OrOlder.apply(lambda x: True if x == 1 else False)

# L Dataframe, W array
df_array = df.to_numpy()

# Nan is no longer my friend, list is now my best friend
def list_rejector(x):
    if str(x).lower() == 'nan':
        return [0]
    else:
        return x.split(',')

# Sorry
def one_liner(line, headers): 
    out_dict = {}
    tl = {'hasPolicy': line[6], 'hasMultiplePolicies': line[7]}
    hi = {'hasPolicy': line[8],'riders': list_rejector(line[9])}

    for i in range(15):
        if i == 6:
            out_dict['termLifeInsurance'] = tl
        elif i == 7:
            continue 
        elif i == 8:
            out_dict['healthInsurance'] = hi   
        elif i == 9:
            continue
        else:
            out_dict[headers[i]] = line[i]
    return out_dict

for row in df_array:
    print(one_liner(row, headers))