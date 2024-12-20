import pandas as pd
import os 
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data by Episode.csv')
cnty = pd.read_csv(dir+'\\countyGISdata.csv')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['END_DATE_TIME'] = pd.to_datetime(df['END_DATE_TIME'])

for i in range(len(df)):
    timediff = df['END_DATE_TIME'][i] - df['BEGIN_DATE_TIME'][i]
    hourdiff = timediff.total_seconds() / 3600
    df.loc[i,'LENGTH_IN_HOURS'] = hourdiff

fig, ax1 = plt.subplots(figsize = (5, 5))
# filtered_df = df[df['DAMAGE_PROPERTY_CPI'] >= 0]
# filtered_df = df[df['EVENT_TYPE'] == 'Ice Storm']

slope, intercept, r, p, se = linregress(df['DAMAGE_PROPERTY_CPI'], df['LENGTH_IN_HOURS'])
plt.grid()
ax1.plot(df['DAMAGE_PROPERTY_CPI'],slope * df['DAMAGE_PROPERTY_CPI'] + intercept,
                         'k--',label=f'Best fit (r={r:.2f})')
ax1.scatter(df['DAMAGE_PROPERTY_CPI'],df['LENGTH_IN_HOURS'],s=8)
ax1.set_xlabel('Property Damage (CPI Adjusted)')
ax1.set_ylabel('Length of Event in Hours')
xticks = ax1.get_xticks()
ax1.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])
# plt.title('Property Damage vs Length of Storm of AR Winter-Related Events')
plt.text(220000000, -12, 'p-value={:.3f}   R={:.3f}   slope={:.3f}'.format(p,r,slope), fontsize=8)
# plt.grid()
# plt.legend()
plt.tight_layout()
plt.savefig(dir+'\\Images\\Damage versus Length of Winter-Related Events.png')