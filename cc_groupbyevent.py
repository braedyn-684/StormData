import pandas as pd
import os 

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

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
    'CZ_NAME': lambda x: ', '.join(sorted(set(x))),  
    'EVENT_TYPE': lambda x: ', '.join(sorted(set(x)))  
}).reset_index()

grouped_df['TOTAL_INJURIES'] = grouped_df['INJURIES_DIRECT'] + grouped_df['INJURIES_INDIRECT']
grouped_df['TOTAL_DEATHS'] = grouped_df['DEATHS_DIRECT'] + grouped_df['DEATHS_INDIRECT']

grouped_df.to_csv(dir+'\\Storm Data by Episode.csv', index=False)

