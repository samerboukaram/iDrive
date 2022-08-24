import json


a = json.load(open('/home/interdrive/Documents/iDrive/Odrive Configurations/ErasedToDefault.json','r'))
b = json.load(open('/home/interdrive/Documents/iDrive/Odrive Configurations/MKR2212Default.json','r'))

import pandas as pd

# df = pd.DataFrame(a)
dfa = pd.json_normalize(a)
dfb = pd.json_normalize(b)
# print(df)
for i in dfa:
    if dfa[i][0] != dfb[i][0]:
     print(i, 'value', dfa[i][0], dfb[i][0])

