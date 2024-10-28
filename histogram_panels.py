import pandas as pd
import os

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\master.csv')

import matplotlib.pyplot as plt
import numpy as np


fig, ax = plt.subplots(1,3, figsize=(15,6))
fig.suptitle('Histograms of winter-related property damage, by county')

ax[0].hist(df['DMGCP2000'])
ax[0].set_ylabel('number of counties')
ax[0].set_title('Jan 1996 to Jun 2005')
ax[0].set_ylim(0,70)
ax[0].set_xlim(0,360000000)
xticks = ax[0].get_xticks()
ax[0].set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])

ax[1].hist(df['DMGCP2010'])
ax[1].set_xlabel('CPI-adjusted property damage ($)')
ax[1].set_title('Jul 2005 to Jun 2015')
ax[1].set_ylim(0,70)
xticks = ax[1].get_xticks()
ax[1].set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])

ax[2].hist(df['DMGCP2020'])
ax[2].set_title('Jul 2015 to Jun 2024')
ax[2].set_ylim(0,70)
xticks = ax[2].get_xticks()
ax[2].set_xticklabels([f'${x/1e3:.0f}K' for x in xticks])
plt.tight_layout()
# plt.show()
plt.savefig(dir+'\\Histograms of damage.png')

# import scipy.stats as stats
# stats.probplot(df['DMGCP2010'], dist="norm", plot=plt)
# plt.show()