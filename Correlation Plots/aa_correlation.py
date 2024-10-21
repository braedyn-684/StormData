import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import linregress
plt.rcParams['font.family'] = 'Arial'

dir = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(dir+'\\master.csv')

VAR_NAME = 'POP2010'
Var_Name = 'Population (2010)'
units = ''
grouping = 'Total'

DMG = np.array(df['DMGCP2010'])
ELEV = np.array(df[VAR_NAME])

fig, ax1 = plt.subplots(figsize = (5, 5))
slope, intercept, r, p, se = linregress(DMG, ELEV)
ax1.scatter(DMG, ELEV, s=5, color='k')
ax1.set_xlabel('Total CPI-adjusted Property Damage 2005-2015 ($)')
ax1.set_xticks(np.linspace(0, 90000000, 5))
xticks = ax1.get_xticks()
ax1.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])
ax1.set_ylabel(grouping+' '+Var_Name+' '+units+'')
plt.text(15000000, -70000, 'p-value={:.3f}   R2={:.3f}   slope={:.3f}'.format(p,r**2,slope), fontsize=8)
plt.plot(DMG,(slope*DMG)+intercept,'b-.')
plt.grid()
plt.tight_layout()
plt.savefig(dir+'\\Correlation Plots\\Damage versus '+Var_Name+'.png')