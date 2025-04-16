import pandas as pd
import os 
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

County = pd.read_csv(dir+'\\CountySize.csv')
counties = County['COUNTY']

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['END_DATE_TIME'] = pd.to_datetime(df['END_DATE_TIME'])


starts = [datetime(2009,  1, 26, 13, 0, 0),
          datetime(2000, 12, 12,  7, 0, 0),
          datetime(2000, 12, 24, 22, 0, 0),
          datetime(2012, 12, 25, 12, 0, 0),
          datetime(2013, 12,  3,  6, 0, 0)]

ends =   [datetime(2009,  1, 28,  5, 0, 0),
          datetime(2000, 12, 13, 17, 0, 0),
          datetime(2000, 12, 26, 22, 0, 0),
          datetime(2012, 12, 26,  7, 0, 0),
          datetime(2013, 12,  6, 20, 0, 0)]

for k in range(len(starts)):
    df2 = df[(df['BEGIN_DATE_TIME']>starts[k]) & (df['END_DATE_TIME']<ends[k])]

    grouped_df = df2.groupby('CZ_NAME').agg({
        'CZ_FIPS': 'first',
        'DAMAGE_PROPERTY': 'sum',
        'DAMAGE_PROPERTY_CPI': 'sum',
    }).reset_index()


    grouped_df.rename(columns={'CZ_NAME': 'COUNTY',
                        'CZ_FIPS': 'FIPS',
                        'DAMAGE_PROPERTY':'DMG',
                        'DAMAGE_PROPERTY_CPI':'DMGCPI'}, inplace=True)
    # grouped_df.set_index('COUNTY')
    df1 = pd.DataFrame(index=counties)
    df1['DMG'] = 0.0
    df1['DMGCPI'] = 0.0

    for county in counties:
        for j in range(len(grouped_df)):
            if county == grouped_df['COUNTY'][j].title():
                df1.loc[county,'DMG'] = grouped_df.loc[j,'DMG']
                df1.loc[county,'DMGCPI'] = grouped_df.loc[j,'DMGCPI']
    # df1 = df1.sort_values(by='COUNTY')
    df1.to_csv(dir+'\\Rank'+str(k+1)+'.csv', index=True)

