import pandas as pd
import os
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data.csv')

# set times to datetimes
df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
for i in range(len(df)):
    if df.loc[i,'END_DAY'] < 10:
        day = '0'+ str(df.loc[i,'END_DAY']) 
    else:
        day = str(df.loc[i,'END_DAY']) 

    if df.loc[i,'END_TIME'] == 0:
        hour = '0000'
    elif df.loc[i,'END_TIME'] < 1000:
        hour = '0'+str(df.loc[i,'END_TIME'])
    else:
        hour = str(df.loc[i,'END_TIME'])
    end_date = str(df.loc[i,'END_YEARMONTH'])+day+' '+hour
    df.loc[i,'END_DATE_TIME'] = datetime.strptime(end_date,'%Y%m%d %H%M')

def convert_damage(value):
  if isinstance(value,str):
    if 'K' in value:
        return float(value.replace('K', '')) * 1000
    elif 'M' in value:
        return float(value.replace('M', '')) * 1000000
    else:
        return float(value)

df['DAMAGE_PROPERTY'] = df['DAMAGE_PROPERTY'].apply(convert_damage)
df['DAMAGE_CROPS'] = df['DAMAGE_CROPS'].apply(convert_damage)

cpi = pd.read_csv(dir+'\\CPI adjustments.csv')

# create a cpi-adjusted property damage column
for i in range(len(df)):
  for j in range(len(cpi)):
    if df.loc[i,'BEGIN_DATE_TIME'].year == cpi.loc[j,'Year']:
        df.loc[i,'DAMAGE_PROPERTY_CPI'] = df.loc[i,'DAMAGE_PROPERTY'] *\
             ((cpi.loc[len(cpi)-1,'Annual'])/(cpi.loc[j,'Annual']))


df.to_csv(dir+'\\Storm Data CPI.csv', index=False)


