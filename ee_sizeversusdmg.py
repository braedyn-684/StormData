import pandas as pd
import os 
import matplotlib.pyplot as plt
from scipy.stats import linregress

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data by Episode.csv')
cnty = pd.read_csv(dir+'\\countyGISdata.csv')

# print(df['CZ_NAME'][0])
for i in range(len(df)):
    area = 0
    for j in range(len(cnty)):
        if cnty.loc[j,'COUNTY'].upper() in df['CZ_NAME'][i]:
            area += cnty.loc[j,'SQ_MILES']
    df.loc[i,'TOTAL_AREA'] = area

fig, ax1 = plt.subplots(figsize = (6, 6))
# filtered_df = df[df['DAMAGE_PROPERTY_CPI'] >= 0]
filtered_df = df[df['EVENT_TYPE'] == 'Ice Storm']

slope, intercept, r, p, se = linregress(filtered_df['DAMAGE_PROPERTY_CPI'], filtered_df['TOTAL_AREA'])

ax1.plot(filtered_df['DAMAGE_PROPERTY_CPI'],slope * filtered_df['DAMAGE_PROPERTY_CPI'] + intercept,
                         'k--',label=f'Best fit (r={r:.2f})')
ax1.scatter(filtered_df['DAMAGE_PROPERTY_CPI'],filtered_df['TOTAL_AREA'],s=8)
ax1.set_xlabel('Property Damage (CPI Adjusted)')
ax1.set_ylabel('Area Affected in Square Miles')
xticks = ax1.get_xticks()
ax1.set_xticklabels([f'${x/1e6:.0f}M' for x in xticks])
plt.title('Property Damage vs Total Area of AR Ice Storm Events')
plt.legend()
plt.savefig(dir+'\\Damage versus Size of Storm Ice Storm.png')