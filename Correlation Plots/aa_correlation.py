import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import linregress
plt.rcParams['font.family'] = 'Arial'

dir = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(dir+'\\master.csv')

DMG = np.array(df['DMGCP'])
ELEV = np.array(df['ELEV'])

fig, ax1 = plt.subplots(figsize = (5, 5))
slope, intercept, r, p, se = linregress(DMG, ELEV)
ax1.scatter(DMG, ELEV, s=5, color='k')
ax1.set_xlabel('Total CPI-adjusted Property Damage ($)')
ax1.set_xticks(np.linspace(0, 400000000, 5))
xticks = ax1.get_xticks()
ax1.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])
ax1.set_ylabel('Mean Elevation (m)')
plt.text(85000000, -50, 'p-value={:.3f}   R2={:.3f}   slope={:.3f}'.format(p,r**2,slope), fontsize=8)
plt.plot(DMG,(slope*DMG)+intercept,'b-.')
plt.grid()
plt.tight_layout()
plt.savefig(dir+'\\Correlation Plots\\Damage versus Elevation.png')