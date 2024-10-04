import pandas as pd
import os 

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])

df['EPISODE_NARRATIVE'] = df['EPISODE_NARRATIVE'].fillna('').astype(str)

for i in range(len(df)):
    if ' ice' in df.loc[i,'EPISODE_NARRATIVE'].lower():
        df.loc[i,'ICE'] = 1
    if 'snow' in df.loc[i,'EPISODE_NARRATIVE'].lower():
        df.loc[i,'SNOW'] = 1

grouped_df = df.groupby('EPISODE_ID').agg({
    'BEGIN_DATE_TIME':'first',
    'END_DATE_TIME':'first',
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
    'EPISODE_NARRATIVE': 'first',  # Assuming the narrative is the same for each EPISODE_ID
    'EVENT_NARRATIVE': 'first',
    'WFO':'first',
    'CZ_NAME': lambda x: ', '.join(sorted(set(x))),  
    'EVENT_TYPE': lambda x: ', '.join(sorted(set(x))),
    'ICE': 'sum',
    'SNOW':'sum'    
}).reset_index()

grouped_df['TOTAL_INJURIES'] = grouped_df['INJURIES_DIRECT'] + grouped_df['INJURIES_INDIRECT']
grouped_df['TOTAL_DEATHS'] = grouped_df['DEATHS_DIRECT'] + grouped_df['DEATHS_INDIRECT']

grouped_df.to_csv(dir+'\\Storm Data by Episode.csv', index=False)

grouped_df['BEGIN_DATE'] = grouped_df['BEGIN_DATE_TIME'].dt.date

grouped_df1 = grouped_df.groupby('BEGIN_DATE').agg({
    'BEGIN_DATE_TIME':'first',
    'END_DATE_TIME':'first',
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
    # 'EPISODE_NARRATIVE':  lambda x: ', '.join(sorted(set(x))),  
    # 'EVENT_NARRATIVE':  lambda x: ', '.join(sorted(set(x))),  
    'WFO': lambda x: ', '.join(sorted(set(x))),  
    'CZ_NAME': lambda x: ', '.join(sorted(set(x))),  
    'EVENT_TYPE': lambda x: ', '.join(sorted(set(x))),
    'ICE': 'sum',
    'SNOW':'sum'  
}).reset_index()

grouped_df1['TOTAL_INJURIES'] = grouped_df1['INJURIES_DIRECT'] + grouped_df1['INJURIES_INDIRECT']
grouped_df1['TOTAL_DEATHS'] = grouped_df1['DEATHS_DIRECT'] + grouped_df1['DEATHS_INDIRECT']

grouped_df1.to_csv(dir+'\\Storm Data by Episode Combined WFO.csv', index=False)



count = 0
for i in range(len(grouped_df1)):
    if ('Ice' in grouped_df1.loc[i,'EVENT_TYPE']) | (grouped_df1.loc[i,'ICE']>0):
        count+=1
ice_per = (count/len(grouped_df1))*100
print('Ice count: '+str(round(ice_per,1))+'%')

count = 0
for i in range(len(grouped_df1)):
    if ('Snow' in grouped_df1.loc[i,'EVENT_TYPE']) | (grouped_df1.loc[i,'SNOW']>0):
        count+=1
snow_per = (count/len(grouped_df1))*100
print('Snow count: '+str(round(snow_per,1))+'%')