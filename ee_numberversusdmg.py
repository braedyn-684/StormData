import pandas as pd
import os 
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\master.csv')


fig, ax1 = plt.subplots(figsize = (5, 5))

slope, intercept, r, p, se = linregress(df['DMGCPI'], df['COUNT'])
plt.grid()
ax1.plot(df['DMGCPI'],slope * df['DMGCPI'] + intercept,
                         'k--',label=f'Best fit (r={r:.2f})')
ax1.scatter(df['DMGCPI'],df['COUNT'],s=8)
ax1.set_xlabel('Property Damage (CPI Adjusted)')
ax1.set_ylabel('Number of Reports')
xticks = ax1.get_xticks()
ax1.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])
# plt.title('Property Damage vs Number of Storm of AR Winter-Related Events')
plt.text(75000000, 4, 'p-value={:.3f}   R={:.3f}   slope={:.3f}'.format(p,r,slope), fontsize=8)
# plt.grid()
# plt.legend()
plt.tight_layout()
plt.savefig(dir+'\\Images\\Damage versus Number of Winter-Related Events.png')