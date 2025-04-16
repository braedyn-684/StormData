import pandas as pd
import os 
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.ticker import ScalarFormatter
# import numpy as np

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data by Episode Combined WFO.csv')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['END_DATE_TIME'] = pd.to_datetime(df['END_DATE_TIME'])

for i in range(len(df)):
    timediff = df['END_DATE_TIME'][i] - df['BEGIN_DATE_TIME'][i]
    hourdiff = timediff.total_seconds() / 3600
    df.loc[i,'LENGTH_IN_HOURS'] = hourdiff


fig, ax1 = plt.subplots(figsize = (5, 5))

# log_y = np.log(df['LENGTH_IN_HOURS'])
slope, intercept, r, p, se = linregress(df['DAMAGE_PROPERTY_CPI'], df['LENGTH_IN_HOURS'])
r=r**2
# ax1.plot(df['DAMAGE_PROPERTY_CPI'],slope * df['DAMAGE_PROPERTY_CPI'] + intercept,
#                          'k--',label=f'Best fit (r={r:.2f})')
plt.text(10000, -27, 'p-value={:.3f}   R\u00b2={:.3f}'.format(p,r), fontsize=8)

ax1.scatter(df['DAMAGE_PROPERTY_CPI'],df['LENGTH_IN_HOURS'],s=8)
ax1.set_xlabel('Property Damage (CPI Adjusted)')
ax1.set_ylabel('Length of Event in Hours')
ax1.set_xscale('log')
formatter = ScalarFormatter()
formatter.set_scientific(False) 
formatter.set_useOffset(False) 
ax1.xaxis.set_major_formatter(formatter)

xticks = ax1.get_xticks()
ax1.set_xticklabels([f'${x:.0f}' for x in xticks],rotation=45)
# plt.title('Property Damage vs Length of Storm of AR Winter-Related Events')
plt.grid()
plt.tight_layout()
plt.savefig(dir+'\\Images\\Damage versus Length of Winter-Related Events.png')