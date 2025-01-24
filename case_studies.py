import pandas as pd
import os 

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['YEAR'] = df['BEGIN_DATE_TIME'].dt.year
df['MONTH'] = df['BEGIN_DATE_TIME'].dt.month

df = df[df['YEAR'] == 2000]
df = df[df['MONTH'] == 12]

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

df1['County_Low'] = df1['COUNTY'].str.title()
print(df1['County_Low'])
df1.to_csv(dir+'\\Storm Data December 2000.csv', index=False)