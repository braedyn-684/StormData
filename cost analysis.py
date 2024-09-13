import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

df = pd.read_csv('C:/Users/dance/Documents/Uark/Masters Project/Storm Data.csv')
months = ['October','November','December','January','February','March','April','May']
event_types = ["Heavy Snow", "Winter Storm", "Winter Weather", "Ice Storm"]


df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])

def convert_damage(value):
  if isinstance(value,str):
    if 'K' in value:
        return float(value.replace('K', '')) * 1000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    else:
        return float(value)

df['DAMAGE_PROPERTY'] = df['DAMAGE_PROPERTY'].apply(convert_damage)
df['DAMAGE_CROPS'] = df['DAMAGE_CROPS'].apply(convert_damage)

years = list(range(1996, 2025))
for i in range(len(df)):
    df.loc[i,'YEAR'] = df.loc[i,'BEGIN_DATE_TIME'].year


yearly_damage = df.groupby('YEAR')[['DAMAGE_PROPERTY', 'DAMAGE_CROPS']].sum()
yearly_damage['TOTAL_DAMAGE'] = yearly_damage['DAMAGE_PROPERTY'] + yearly_damage['DAMAGE_CROPS']


fig, ax =plt.subplots(figsize=(12,5))
ax.plot(yearly_damage.index,yearly_damage['TOTAL_DAMAGE'], color='blue')
plt.title('Yearly Crop & Property Winter-Related Damage reported on *StormData* (1996-2024)')
plt.ylim(0,800000000)
yticks = ax.get_yticks()
ax.set_yticklabels([f'${y/1e6:.0f}M' for y in yticks])
plt.xlim(1996,2024)
ax.set_xticks(range(1996, 2025))
plt.xticks(rotation=45)
# plt.grid(True)
plt.tight_layout()
