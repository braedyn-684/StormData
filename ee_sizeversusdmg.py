import pandas as pd
import os 
import matplotlib.pyplot as plt

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

cnty = pd.read_csv(dir+'\\countyGISdata.csv')

for i in range(len(df)):
  for j in range(len(cnty)):
    if df.loc[i,'COUNTY']==cnty.loc[j,'COUNTY'].upper():
        df.loc[i,'AREA'] = cnty.loc[j,'SQ_MILES']

plt.scatter(df['DMGPRPCPI'])