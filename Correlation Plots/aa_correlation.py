import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.stats import linregress
plt.rcParams['font.family'] = 'Arial'

dir = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(dir+'\\master.csv')

VAR_NAME = ['POP2000','POP2010','POP2020']
Var_Name = ['Population (2000)','Population (2010)','Population (2020)']
Dep_Name = ['DMGCP2000','DMGCP2010','DMGCP2020']
units = ''
grouping = 'Total'
VAR_NAME = ['COUNT']
Var_Name = ['Number of Reports']
Dep_Name = ['DMGCPI']

for i in range(len(Var_Name)):
    DMG = np.array(df[Dep_Name[i]])
    ELEV = np.array(df[VAR_NAME[i]])
    fig, ax1 = plt.subplots(figsize = (5, 5))
    slope, intercept, r, p, se = linregress(DMG, ELEV)
    ax1.scatter(DMG, ELEV, s=5, color='k')

    

    ax1.set_ylabel(grouping+' '+Var_Name[i]+' '+units+'')
    if VAR_NAME[i] == 'POP2000':
        yticks = ax1.get_yticks()
        ax1.set_yticklabels([f'{y/1e3:.0f}K' for y in yticks])  
        ax1.set_xlabel('Total CPI-adjusted Property Damage 1996-2005 ($)')
        ax1.set_xticks(np.linspace(0, 400000000, 5))
        xticks = ax1.get_xticks()
        ax1.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])
        plt.text(70000000, -70000, 'p-value={:.3f}   R={:.3f}   slope={:.3f}'.format(p,r,slope), fontsize=8)
    if VAR_NAME[i] == 'POP2010':
        yticks = ax1.get_yticks()
        ax1.set_yticklabels([f'{y/1e3:.0f}K' for y in yticks])
        ax1.set_xlabel('Total CPI-adjusted Property Damage 2005-2015 ($)')
        ax1.set_xticks(np.linspace(0, 90000000, 5))
        xticks = ax1.get_xticks()
        ax1.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])
        plt.text(15000000, -70000, 'p-value={:.3f}   R={:.3f}   slope={:.3f}'.format(p,r,slope), fontsize=8)
    if VAR_NAME[i] == 'POP2020':
        yticks = ax1.get_yticks()
        ax1.set_yticklabels([f'{y/1e3:.0f}K' for y in yticks])
        xticks = ax1.get_xticks()
        ax1.set_xlabel('Total CPI-adjusted Property Damage 2015-2024 ($)')
        ax1.set_xticks(np.linspace(0, 700000, 5))
        xticks = ax1.get_xticks()
        ax1.set_xticklabels([f'${x/1e3:.0f}K' for x in xticks])
        plt.text(100000, -70000, 'p-value={:.3f}   R={:.3f}   slope={:.3f}'.format(p,r,slope), fontsize=8)
    if VAR_NAME[i] == 'COUNT':
        yticks = ax1.get_yticks()
        ax1.set_yticklabels([f'{y:.0f}' for y in yticks])
        xticks = ax1.get_xticks()
        ax1.set_xlabel('Total CPI-adjusted Property Damage 1996-2024 ($)')
        ax1.set_xticks(np.linspace(0, 400100000, 5))
        xticks = ax1.get_xticks()
        ax1.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])
        plt.text(90000000, 5, 'p-value={:.3f}   R={:.3f}   slope={:.3f}'.format(p,r,slope), fontsize=8)
    plt.plot(DMG,(slope*DMG)+intercept,'b-.')
    plt.grid()
    plt.tight_layout()
    plt.savefig(dir+'\\Correlation Plots\\Damage versus '+Var_Name[i]+'.png')