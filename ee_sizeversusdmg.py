import pandas as pd
import os 
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib.ticker import ScalarFormatter

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data by Episode Combined WFO.csv')
cnty = pd.read_csv(dir+'\\countyGISdata.csv')

# print(df['CZ_NAME'][0])
for i in range(len(df)):
    area = 0
    cntys = df['CZ_NAME'][i].split(', ')
    unique_cntys = list(set(cntys))
    for j in range(len(cnty)):
        if cnty.loc[j,'COUNTY'].upper() in unique_cntys:
            area += cnty.loc[j,'SQ_MILES']
    df.loc[i,'TOTAL_AREA'] = area

fig, ax1 = plt.subplots(figsize = (5, 5))

slope, intercept, r, p, se = linregress(df['DAMAGE_PROPERTY_CPI'], df['TOTAL_AREA'])
r=r**2

# ax1.plot(df['DAMAGE_PROPERTY_CPI'],slope * df['DAMAGE_PROPERTY_CPI'] + intercept,
#                          'k--',label=f'Best fit (r={r:.2f})')
ax1.scatter(df['DAMAGE_PROPERTY_CPI'],df['TOTAL_AREA'],s=8)
ax1.set_xlabel('Property Damage (CPI Adjusted)')
ax1.set_ylabel('Area Affected in Square Miles')
ax1.set_xscale('log')
formatter = ScalarFormatter()
formatter.set_scientific(False) 
formatter.set_useOffset(False) 
ax1.xaxis.set_major_formatter(formatter)

xticks = ax1.get_xticks()
ax1.set_xticklabels([f'${x:.0f}' for x in xticks],rotation=45)
yticks = ax1.get_yticks()
ax1.set_yticklabels([f'{y/1e3:.0f}K' for y in yticks])
plt.grid()
# plt.title('Property Damage vs Total Area of AR Winter-Related Events')
plt.text(10000, -23000, 'p-value={:.3f}   R\u00b2={:.3f}'.format(p,r), fontsize=8)
# plt.legend()
plt.tight_layout()
plt.savefig(dir+'\\Images\\CPI-adjusted Damage versus Size of Storms.png')


# df = df[df['DAMAGE_PROPERTY_CPI']>37000000]
# fig, ax2 = plt.subplots(figsize = (5, 5))
# ax2.scatter(df['DAMAGE_PROPERTY_CPI'],df['TOTAL_AREA'],s=8)
# ax2.set_xlabel('Property Damage (CPI Adjusted)')
# ax2.set_ylabel('Area Affected in Square Miles')
# xticks = ax2.get_xticks()
# ax2.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks],rotation=45)
# yticks = ax2.get_yticks()
# ax2.set_yticklabels([f'{y/1e3:.0f}K' for y in yticks])
# plt.grid()
# plt.tight_layout()
# plt.savefig(dir+'\\Images\\Most Expensive Damage versus Size.png')