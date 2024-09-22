import pandas as pd
import os 
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

grouped_df = df.groupby('CZ_NAME').agg({
    'CZ_FIPS': 'first',
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
}).reset_index()

grouped_df['TOTAL_INJURIES'] = grouped_df['INJURIES_DIRECT'] + grouped_df['INJURIES_INDIRECT']
grouped_df['TOTAL_DEATHS'] = grouped_df['DEATHS_DIRECT'] + grouped_df['DEATHS_INDIRECT']


grouped_df.rename(columns={'CZ_NAME': 'COUNTY',
                    'CZ_FIPS': 'FIPS',
                    'INJURIES_DIRECT': 'DIRINJ',
                    'INJURIES_INDIRECT':'INDIRINJ',
                    'DEATHS_DIRECT':'DIRDTH',
                    'DEATHS_INDIRECT':'INDIRDTH',
                    'DAMAGE_PROPERTY':'DMGPRP',
                    'DAMAGE_PROPERTY_CPI':'DMGPRPCPI'}, inplace=True)


df1 = grouped_df

df1 = df1.sort_values(by='COUNTY')
df1.to_csv(dir+'\\Storm Data by County.csv', index=False)



dates = [datetime(1995,6,30), datetime(2005,6,30), datetime(2015,6,30), datetime(2025,6,30)]
date_name = ['2000','2010','2020']
for i in range(len(date_name)):
    df = pd.read_csv(dir+'\\Storm Data CPI.csv')
    df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
    df = df[(df['BEGIN_DATE_TIME']>=dates[i]) & (df['BEGIN_DATE_TIME']<dates[i+1])]
    grouped_df1 = df.groupby('CZ_NAME').agg({
        'CZ_FIPS': 'first',
        'INJURIES_DIRECT': 'sum',
        'INJURIES_INDIRECT': 'sum',
        'DEATHS_DIRECT': 'sum',
        'DEATHS_INDIRECT': 'sum',
        'DAMAGE_PROPERTY': 'sum',
        'DAMAGE_PROPERTY_CPI': 'sum',
    }).reset_index()

    grouped_df1['TOTAL_INJURIES'] = grouped_df1['INJURIES_DIRECT'] + grouped_df1['INJURIES_INDIRECT']
    grouped_df1['TOTAL_DEATHS'] = grouped_df1['DEATHS_DIRECT'] + grouped_df1['DEATHS_INDIRECT']


    grouped_df1.rename(columns={'CZ_NAME': 'COUNTY',
                        'CZ_FIPS': 'FIPS',
                        'INJURIES_DIRECT': 'DIRINJ',
                        'INJURIES_INDIRECT':'INDIRINJ',
                        'DEATHS_DIRECT':'DIRDTH',
                        'DEATHS_INDIRECT':'INDIRDTH',
                        'DAMAGE_PROPERTY':'DMGPRP',
                        'DAMAGE_PROPERTY_CPI':'DMGPRPCPI'}, inplace=True)


    df2 = grouped_df1

    df2 = df2.sort_values(by='COUNTY')
    df2.to_csv(dir+'\\Storm Data by County '+date_name[i]+'.csv', index=False)
