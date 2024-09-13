import pandas as pd
import os 

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


df = grouped_df
# for i in range(len(new)):
#     row = df[df['COUNTY'].isin([original[i], new[i]])].sum()
#     row['COUNTY'] = original[i]
#     row['FIPS'] = df[df['COUNTY'] == original[i]]['FIPS'].values[0]        
#     df = df[~df['COUNTY'].isin([original[i], new[i]])]
#     row_df = pd.DataFrame([row])  
#     df = pd.concat([df, row_df], ignore_index=True)


df = df.sort_values(by='COUNTY')
df.to_csv(dir+'\\Storm Data by County.csv', index=False)
