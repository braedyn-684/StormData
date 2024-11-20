import pandas as pd
import os 
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import datetime, timedelta

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data by Episode.csv')
cnty = pd.read_csv(dir+'\\countyGISdata.csv')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['END_DATE_TIME'] = pd.to_datetime(df['END_DATE_TIME'])

df['WEEKDAYS'] = None
df['WEEKDAY_NAMES'] = None
for i in range(len(df)):
    startdate = df.loc[i,'BEGIN_DATE_TIME']
    enddate = df.loc[i,'END_DATE_TIME']

    weekdays=[]
    names=[]
    current = startdate
    while current <= enddate:
        weekdays.append(current.weekday())
        names.append(current.strftime('%a'))
        current += timedelta(days=1)

    df.at[i,'WEEKDAYS'] = weekdays
    df.at[i,'WEEKDAY_NAMES'] = names


    midpoint = startdate + (enddate - startdate) / 2
    df.loc[i,'MEDIAN WEEKDAY'] = midpoint.weekday()
    df.loc[i,'MEDIAN WEEKDAY NAME'] = midpoint.strftime('%a')


weekday_order = [0,1,2,3,4,5,6]
weekdays = ['Mon','Tue','Wed','Thur','Fri','Sat','Sun']
funding_by_weekday = df.groupby(['MEDIAN WEEKDAY'])['DAMAGE_PROPERTY_CPI'].sum()

funding_by_weekday = funding_by_weekday.loc[weekday_order]

fig, ax1 = plt.subplots(figsize = (8, 6))
funding_by_weekday.plot(kind='bar',color='skyblue',ax=plt.gca())
ax1.set_xticks(range(len(weekdays)))
ax1.set_xticklabels(weekdays)
plt.title('Damage by median weekday in Arkansas with CPI adjustment')
plt.ylabel('Total CPI-adjusted property damage ($)')
plt.xticks(rotation=0)
plt.xlabel('')
yticks = ax1.get_yticks()
ax1.set_yticklabels([f'${y/1e6:.0f}M' for y in yticks])
plt.savefig(dir+'\\Images\\Damage by weekday bar plots.png')

# print(weekdays)
