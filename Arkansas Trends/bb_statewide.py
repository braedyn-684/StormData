import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))

vars = ['Precip','Max Temp','Min Temp']
names = ['precipitation','max temperature','minimum temperature']
units = ['(in)','(F)','(F)']

fig, ax = plt.subplots(1,3, figsize=(16,6))
fig.suptitle('Trends in Arkansas from 1900-2024')

for i in range(3):
    df = pd.read_csv(dir+'\\Arkansas Trends/Statewide '+vars[i]+'.csv')
    for j in range(len(df)):
        df.loc[j,'Date'] = datetime.strptime(str(df.loc[j,'Date']), "%Y%m")


    df['Date'] = pd.to_datetime(df['Date'])
    x=df['Date']
    y=df['Value']
    X=np.array(df.index)
    Y=np.array(df['Value'])
    slope, intercept, r, p, se = linregress(X,Y)

    ax[i].plot(x,y)
    ax[i].plot(x,slope*X+intercept,'k--')
    ax[i].set_xlabel('p-value={:.3f}   R2={:.1f}   slope={:.3f}'.format(p,r,slope))
    ax[i].set_ylabel(names[i]+' '+units[i])


plt.tight_layout()
# plt.show()
plt.savefig(dir+'\\Arkansas Trends/Statewide Trends.png')