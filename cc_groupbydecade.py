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

df_2000.to_csv(dir+'\\Storm Data CPI 2000.csv', index=False)
df_2010.to_csv(dir+'\\Storm Data CPI 2010.csv', index=False)
df_2020.to_csv(dir+'\\Storm Data CPI 2020.csv', index=False)

