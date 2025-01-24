import pandas as pd
import numpy as np
import os 
import matplotlib.pyplot as plt
from scipy.stats import linregress

dir = os.path.dirname(os.path.abspath(__file__))
# df = pd.read_csv(dir+'\\Storm Data CPI.csv')
df = pd.read_csv(dir+'\\Storm Data by Episode Combined WFO.csv')
# df = df[df['EVENT_TYPE'] != 'Winter Weather']

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])

df['YEAR'] = df['BEGIN_DATE_TIME'].dt.year
df['ID'] = df.index

# yearly_events = df.groupby('YEAR')['EPISODE_ID'].nunique().sort_index()
yearly_events = df.groupby('YEAR')['ID'].nunique().sort_index()
years = list(range(1996, 2025))
fig, ax1 = plt.subplots(figsize = (10, 6))
plt.bar(years, yearly_events.tolist(), color='skyblue')

plt.ylabel('Number of winter-related events')

plt.title('Number of winter-related events by year in AR (1996-2024)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

years = yearly_events.index.tolist()
slope, intercept, r, p, se = linregress(years, yearly_events.tolist())
best_fit = [slope * year + intercept for year in years]

plt.plot(years, best_fit, 'k--', label=f'Best fit (r={r:.2f})')
plt.xlabel('p-value={:.3f}   R2={:.1f}   slope={:.3f}'.format(p,r,slope))
plt.xticks(np.arange(1996,2025,4)) 

plt.tight_layout()
# plt.show()
plt.savefig(dir+'\\Images\\Yearly bar plots.png')



yearly_damage = df.groupby('YEAR')['DAMAGE_PROPERTY_CPI'].sum().sort_index()
years = list(range(1996, 2025))
fig, ax1 = plt.subplots(figsize = (10, 6))
plt.bar(years, yearly_damage.tolist(), color='blue')

plt.ylabel('Winter-related damage per year')

plt.title('Winter-related, CPI-adjusted damage by year in AR (1996-2024)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

years = yearly_damage.index.tolist()
slope, intercept, r, p, se = linregress(years, yearly_damage.tolist())
best_fit = [slope * year + intercept for year in years]
yticks = ax1.get_yticks()
ax1.set_yticklabels([f'${y/1e6:.0f}M' for y in yticks])

plt.plot(years, best_fit, 'k--', label=f'Best fit (r={r:.2f})')
plt.xlabel('p-value={:.3f}   R2={:.1f}   slope={:.3f}'.format(p,r,slope))
plt.xticks(np.arange(1996,2025,4)) 

plt.tight_layout()
# plt.show()
plt.savefig(dir+'\\Images\\Yearly bar plots dmg.png')