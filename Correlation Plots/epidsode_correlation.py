import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from datetime import datetime, timedelta
dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data by Episode Combined WFO.csv')

size = pd.read_csv(dir+'\\CountySize.csv')

for i in range(len(df)):
    area = 0
    for j in range(len(size)):
        if size.loc[j,'COUNTY'].upper() in df['CZ_NAME'][i]:
            area += size.loc[j,'SQ_MILES']
    df.loc[i,'TOTAL_AREA'] = area
# print(df['TOTAL_AREA'])

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['END_DATE_TIME'] = pd.to_datetime(df['END_DATE_TIME'])

df['WEEKDAYS'] = None
df['WEEKDAY_NAMES'] = None
for i in range(len(df)):
    startdate = df.loc[i,'BEGIN_DATE_TIME']
    enddate = df.loc[i,'END_DATE_TIME']

    difference = enddate - startdate
    midpoint = startdate + (difference/2)

    df.loc[i,'MEDIAN WEEKDAY'] = midpoint.weekday()
    df.loc[i,'MEDIAN WEEKDAY NAME'] = midpoint.strftime('%A')

    df.loc[i,'LENGTH OF STORM'] = difference.total_seconds()/3600




# from sklearn.preprocessing import StandardScaler
# scaler = StandardScaler()
# scaled_data = scaler.fit_transform(df)
# scaled_df = pd.DataFrame(scaled_data, columns=df.columns)

Y = df['DAMAGE_PROPERTY_CPI']
X = df[['LENGTH OF STORM','MEDIAN WEEKDAY','TOTAL_AREA']]

X = sm.add_constant(X)
model = sm.OLS(Y,X).fit()
print(model.summary())