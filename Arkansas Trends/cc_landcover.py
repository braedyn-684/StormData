import pandas as pd
import os
import numpy as np

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Arkansas Trends/land cover.csv')
# df['landcover Count'] = df['landcover Count'].astype('float')
sum = df['landcover Count'].sum()
for i in range(len(df)):
    df.loc[i,'Percent'] = (df.loc[i,'landcover Count']/sum)* 100

df.to_csv(dir+'\\Arkansas Trends/Land Cover Percents.csv')