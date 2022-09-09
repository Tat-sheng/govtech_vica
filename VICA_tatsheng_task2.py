# Misc
import warnings
warnings.filterwarnings('ignore')

import json
import pandas as pd
import numpy as np
from pymongo import MongoClient

# Instructions
#  - You can run the code to print to review the structured format
#  - You can uncomment the highlighted chunks and insert your URL to import the data into your MongoDB

# Uncomment below ===========================================================
# CONNECTION_URL = "mongodb://root:rootpassword@localhost:27017"
# db = MongoClient(host = CONNECTION_URL)
# ===========================================================================

# Load and store 
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

# Convert to array for easier manipulation
df_array = df.to_numpy()

# Nan is no longer my friend, list is now my best friend
def list_rejector(x):
    if str(x).lower() == 'nan':
        return [0]
    else:
        return x.split(',')

# Structure function
def one_liner(line, headers): 
    out_dict = {}
    tl = {'hasPolicy': line[6], 'hasMultiplePolicies': line[7]}
    hi = {'hasPolicy': line[8],'riders': list_rejector(line[9])}

    for i in range(15): # 15 is the length of headers list 
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
    # Uncomment below =======================================================
    # db.segment.insert(json.dumps(one_liner(row, headers)))
    # =======================================================================

# The structured code is original but for the DB insertions (Line 15,16 & 67), I took reference to 
# https://webdamn.com/import-csv-file-into-mongodb-using-python/
#                                                                                      - Tat Sheng