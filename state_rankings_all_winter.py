import pandas as pd
import os
import locale
locale.setlocale(locale.LC_ALL, '')
from datetime import datetime
dir = os.path.dirname(os.path.abspath(__file__))
stormevents_dir = os.path.join(dir, "StormEvents")
all_files = os.listdir(stormevents_dir)
csv_files = [file for file in all_files if file.endswith('.csv')]

event_types = ["Blizzard","Lake-Effect Snow","Sleet","Heavy Snow", 
               "Winter Storm", "Winter Weather", "Ice Storm"]

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

combined_df = pd.merge(combined_df, cpi[['Year', 'Annual']], on='Year', how='left')
combined_df['DAMAGE_PROPERTY_CPI'] = combined_df['DAMAGE_PROPERTY'] *\
    (cpi.loc[len(cpi)-1,'Annual'] / combined_df['Annual'])


ALL = combined_df.groupby('STATE').agg({
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
}).reset_index()

States = ALL['STATE']
ALL.set_index('STATE', inplace=True)

# var = ['DD','ID','DI','II','CPI']
# var_full = ['DEATHS_DIRECT','DEATHS_INDIRECT','INJURIES_DIRECT',
#             'INJURIES_INDIRECT','DAMAGE_PROPERTY_CPI']
# var_names = ['Direct Deaths','Indirect Deaths','Direct Injuries',
#              'Indirect Injuries','CPI-Adj. Damage']

# def ordinal(n):
#     if 10 <= n % 100 <= 20:
#         suffix = 'th'
#     else:
#         suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
#     return str(n) + suffix

# for v in range(5): 
#     df['ALL'+' '+var[v]] = ALL[var_full[v]]
# for v in range(5): 
#     df['ALL'+' '+var[v]+' Rank'] = df['ALL'+' '+var[v]].rank(ascending=False,method='max')

# rank_one_data = []
# for v in range(5): 
#     top_state = df[df['ALL'+' '+var[v]+' Rank'] == 1.0].index#.tolist()
#     rank = 1
#     if v == 4:
#         value = locale.currency(df.loc[top_state[0],'ALL'+' '+var[v]],grouping=True)
#     else:
#         value = str(df.loc[top_state[0],'ALL'+' '+var[v]])
#     rank_one_data.append({
#         'Event': 'All',
#         'Variable': var_names[v],
#         'State': top_state[0],
#         'Rank': ordinal(rank),
#         'Value':value
#     })

# rank_one_df = pd.DataFrame(rank_one_data)
# print(rank_one_df)
ALL.to_csv(dir+'\\All Winter Types Ranking.csv', index=True)