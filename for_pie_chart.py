import pandas as pd
import os
dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\AR All Types.csv')

event_types = ["Blizzard","Lake-Effect Snow","Sleet","Heavy Snow", 
               "Winter Storm", "Winter Weather", "Ice Storm",
               "Extreme Cold/Wind Chill", "Cold/Wind Chill"]

event_counts = df[df['EVENT_TYPE'].isin(event_types)]['EVENT_TYPE'].value_counts()
print(event_counts)

event_total_dmg = df.groupby('EVENT_TYPE')['DAMAGE_PROPERTY_CPI'].sum()
print(event_total_dmg)