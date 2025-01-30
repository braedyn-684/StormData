import pandas as pd
import os
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])

date0 = datetime(2005,6,30)
date1 = datetime(2015,6,30)

df_2000 = df[df['BEGIN_DATE_TIME']<date0]
df_2010 = df[(df['BEGIN_DATE_TIME']>date0)&(df['BEGIN_DATE_TIME']<date1)]
df_2020 = df[df['BEGIN_DATE_TIME']>date1]


df0 = pd.read_csv(dir+'\\Storm Data by County.csv')
counties = df0['COUNTY']

df1 = pd.DataFrame(index=counties)

for county in counties:
    df_0 = df_2000[df_2000['CZ_NAME']==county]
    df_dmg0 = df_0[df_0['DAMAGE_PROPERTY_CPI']>0]
    df1.loc[county,'PerRep00'] = (len(df_dmg0)/len(df_0))*100

    df_1 = df_2010[df_2010['CZ_NAME']==county]
    df_dmg1 = df_1[df_1['DAMAGE_PROPERTY_CPI']>0]
    df1.loc[county,'PerRep10'] = (len(df_dmg1)/len(df_1))*100

    df_2 = df_2020[df_2020['CZ_NAME']==county]
    df_dmg2 = df_2[df_2['DAMAGE_PROPERTY_CPI']>0]
    df1.loc[county,'PerRep20'] = (len(df_dmg2)/len(df_2))*100
    
df1.to_csv(dir+'/Percent_Reporting.csv')