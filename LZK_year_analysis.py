import pandas as pd
import os
import numpy as np
# from datetime import datetime
import matplotlib.pyplot as plt
# from scipy.stats import linregress

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\TSA Storm Data.csv')
df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['YEAR'] = df['BEGIN_DATE_TIME'].dt.year

def convert_damage(value):
  if isinstance(value,str):
    if 'K' in value:
        return float(value.replace('K', '')) * 1000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    else:
        return float(value)
df['DAMAGE_PROPERTY'] = df['DAMAGE_PROPERTY'].apply(convert_damage) 

grouped_df = df.groupby('YEAR').agg({
    'INJURIES_DIRECT': 'sum',
    'INJURIES_INDIRECT': 'sum',
    'DEATHS_DIRECT': 'sum',
    'DEATHS_INDIRECT': 'sum',
    'DAMAGE_PROPERTY': 'sum',
}).reset_index()

df1 = grouped_df.sort_values(by='YEAR')


fig, ax1 = plt.subplots(figsize = (10, 6))
plt.bar(df1['YEAR'], df1['DAMAGE_PROPERTY'], color='skyblue')
plt.xticks(np.arange(1996,2025,4)) 
plt.yscale('log')
plt.ylim(0,1000000000)
# plt.ylim(0,10000)
yticks = ax1.get_yticks()
ax1.set_yticklabels([f'${y/1e6:.0f}M' for y in yticks])
plt.title('Winter-Related Property Damage Reported by TSA/Arkansas')
plt.grid()
plt.tight_layout()
# slope, intercept, r, p, se = linregress(df1['YEAR'], df['DAMAGE_PROPERTY'])
# best_fit = [slope * year + intercept for year in years]

plt.savefig(dir+'\\Images\\TSA Damage.png')