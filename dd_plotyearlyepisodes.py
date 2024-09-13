import pandas as pd
import os 
import matplotlib.pyplot as plt
from scipy.stats import linregress

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])

df['YEAR'] = df['BEGIN_DATE_TIME'].dt.year

yearly_events = df.groupby('YEAR')['EPISODE_ID'].nunique().sort_index()
years = list(range(1996, 2025))
fig, ax1 = plt.subplots(figsize = (10, 6))
plt.bar(years, yearly_events.tolist(), color='skyblue')

plt.ylabel('Number of winter-related events')
plt.xlabel('')
plt.title('Number of winter-related events by year in AR (1996-2024)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)

years = yearly_events.index.tolist()
slope, intercept, r, p, se = linregress(years, yearly_events.tolist())
best_fit = [slope * year + intercept for year in years]

plt.plot(years, best_fit, 'k--', label=f'Best fit (r={r:.2f})')


plt.tight_layout()
plt.savefig(dir+'\\Yearly bar plots.png')


