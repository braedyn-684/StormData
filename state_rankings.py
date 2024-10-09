import pandas as pd
import os
from datetime import datetime
dir = os.path.dirname(os.path.abspath(__file__))
stormevents_dir = os.path.join(dir, "StormEvents")
all_files = os.listdir(stormevents_dir)
csv_files = [file for file in all_files if file.endswith('.csv')]

event_types = ["Heavy Snow", "Winter Storm", "Winter Weather", "Ice Storm"]

dfs=[]
for csv_file in csv_files:
    df = pd.read_csv(stormevents_dir+'/'+csv_file)
    df = df[df['EVENT_TYPE'].isin(event_types)]
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

combined_df['BEGIN_DATE_TIME'] = pd.to_datetime(combined_df['BEGIN_DATE_TIME'])#, format='%Y%m')
combined_df['Year'] = combined_df['BEGIN_DATE_TIME'].dt.year

def convert_damage(value):
  if isinstance(value,str):
    if 'K' in value:
        return float(value.replace('K', '')) * 1000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    else:
        return float(value)
    
combined_df['DAMAGE_PROPERTY'] = combined_df['DAMAGE_PROPERTY'].apply(convert_damage)
combined_df['DAMAGE_CROPS'] = combined_df['DAMAGE_CROPS'].apply(convert_damage)

cpi = pd.read_csv(dir+'\\CPI adjustments.csv')
# for i in range(len(combined_df)):
#   for j in range(len(cpi)):
#     if combined_df.loc[i,'BEGIN_DATE_TIME'].year == cpi.loc[j,'Year']:
#         combined_df.loc[i,'DAMAGE_PROPERTY_CPI'] = combined_df.loc[i,'DAMAGE_PROPERTY'] *\
#              ((cpi.loc[len(cpi)-1,'Annual'])/(cpi.loc[j,'Annual']))

combined_df = pd.merge(combined_df, cpi[['Year', 'Annual']], on='Year', how='left')
combined_df['DAMAGE_PROPERTY_CPI'] = combined_df['DAMAGE_PROPERTY'] *\
    (cpi.loc[len(cpi)-1,'Annual'] / combined_df['Annual'])


HS = combined_df[combined_df['EVENT_TYPE']=='Heavy Snow']
grouped_HS = HS.groupby('STATE').agg({
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
}).reset_index()
grouped_HS.to_csv(dir+'\\State Rankings Heavy Snow.csv', index=False)

WS = combined_df[combined_df['EVENT_TYPE']=='Winter Storm']
grouped_WS = WS.groupby('STATE').agg({
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
}).reset_index()
grouped_WS.to_csv(dir+'\\State Rankings Winter Storm.csv', index=False)


WW = combined_df[combined_df['EVENT_TYPE']=='Winter Weather']
grouped_WW = WW.groupby('STATE').agg({
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
}).reset_index()
grouped_WW.to_csv(dir+'\\State Rankings Winter Weather.csv', index=False)

IS = combined_df[combined_df['EVENT_TYPE']=='Ice Storm']
grouped_IS = IS.groupby('STATE').agg({
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
}).reset_index()
grouped_IS.to_csv(dir+'\\State Rankings Ice Storm.csv', index=False)


grouped = combined_df.groupby('STATE').agg({
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
}).reset_index()
grouped.to_csv(dir+'\\State Rankings.csv', index=False)