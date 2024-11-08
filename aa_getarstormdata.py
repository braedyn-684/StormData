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
    df = df[df['STATE']=='ARKANSAS']
    df = df[df['EVENT_TYPE'].isin(event_types)]
    dfs.append(df)


combined_df = pd.concat(dfs, ignore_index=True)





for i in range(len(combined_df)):
    if combined_df.loc[i,'CZ_NAME'] == '"EASTERN, CENTRAL AND SOUTHERN SEARCY COUNTY HIGHER ELEVATIONS"':
        combined_df.loc[i,'CZ_NAME'] = 'EASTERN, CENTRAL AND SOUTHERN SEARCY COUNTY HIGHER ELEVATIONS'

original = ['BOONE','MONTGOMERY','SCOTT','SEARCY',
            'JOHNSON','NEWTON','NEWTON','MONTGOMERY',
            'POLK','SCOTT','SEARCY','YELL','POLK',
            'POPE','SEARCY','POLK','VAN BUREN',
            'LOGAN','JOHNSON','POPE','VAN BUREN',
            'LOGAN','YELL']
new = ['BOONE COUNTY EXCEPT SOUTHWEST','CENTRAL AND EASTERN MONTGOMERY COUNTY',
       'CENTRAL AND SOUTHERN SCOTT COUNTY','EASTERN, CENTRAL AND SOUTHERN SEARCY COUNTY HIGHER ELEVATIONS',
       'JOHNSON COUNTY HIGHER ELEVATIONS','NEWTON COUNTY HIGHER ELEVATIONS',
       'NEWTON COUNTY LOWER ELEVATIONS','NORTHERN MONTGOMERY COUNTY HIGHER ELEVATIONS',
       'NORTHERN POLK COUNTY HIGHER ELEVATIONS','NORTHERN SCOTT COUNTY',
       'NORTHWEST SEARCY COUNTY HIGHER ELEVATIONS','NORTHWEST YELL COUNTY',
       'POLK COUNTY LOWER ELEVATIONS',
       'POPE COUNTY HIGHER ELEVATIONS','SEARCY COUNTY LOWER ELEVATIONS',
       'SOUTHEAST POLK COUNTY HIGHER ELEVATIONS','SOUTHEAST VAN BUREN COUNTY',
       'SOUTHERN AND EASTERN LOGAN COUNTY','SOUTHERN JOHNSON COUNTY',
       'SOUTHERN POPE COUNTY','VAN BUREN COUNTY HIGHER ELEVATIONS',
       'WESTERN AND NORTHERN LOGAN COUNTY','YELL COUNTY EXCLUDING NORTHWEST']

for i in range(len(combined_df)):
    for j in range(len(original)):
        if combined_df.loc[i,'CZ_NAME'] == new[j]:
            combined_df.loc[i,'CZ_NAME'] = original[j]

combined_df.to_csv(dir+'\\Storm Data.csv', index=False)

