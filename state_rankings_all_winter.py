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
               "Winter Storm", "Winter Weather", "Ice Storm",
               "Extreme Cold/Wind Chill", "Cold/Wind Chill"]

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

df2 = combined_df[combined_df['STATE']=='ARKANSAS']
df2.to_csv(dir+'\\AR All Types.csv', index=False)

ALL = combined_df.groupby('STATE').agg({
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
    'DAMAGE_PROPERTY_CPI': 'sum',
}).reset_index()

def capitalize(item):
    # new_list=[]
    # for item in lst:
        words = item.split()
        new_words = ' '.join([word.capitalize() if word != 'OF' else word.lower() for word in words])
        return new_words
    #     new_list.append(new_words)
    # return new_list

for i in range(len(ALL)):
    ALL.loc[i,'Name'] = capitalize(ALL.loc[i,'STATE'])
states = ALL['Name']
ALL.set_index('Name', inplace=True)


pop = pd.read_csv(dir+'\\US Population by state.csv')
pop = pop.set_index('State')
for state in states:
    if state != 'Virgin Islands':
        ALL.loc[state,'POP'] = pop.loc[state,'Total']

ALL['DMGPOP2020'] = ALL['DAMAGE_PROPERTY_CPI']/ALL['POP']

ALL.to_csv(dir+'\\All Winter Types Ranking.csv', index=True)