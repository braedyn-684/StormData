import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))

vars = ['Precip', 'Avg Temp']#'Max Temp','Min Temp',
names = ['precipitation','avg temperature']#'max temperature','minimum temperature']
units = ['(mm)','(C)']#,'(F)']

def f_to_c(temp):
    return (temp - 32)*(5/9)

def in_to_mm(precip):
    return (precip*25.4)

fig, ax = plt.subplots(1,len(vars), figsize=(11,6))
fig.suptitle('Trends in Arkansas from 1900-2024')

for i in range(len(vars)):
    df = pd.read_csv(dir+'\\Arkansas Trends/Statewide '+vars[i]+'.csv')
    if vars[i] == 'Avg Temp':
        df['Converted'] = f_to_c(df['Value'])
        
    if vars[i] == 'Precip':
        df['Converted'] = in_to_mm(df['Value'])


    df['month'] = pd.to_datetime(df['Date']).dt.month
    for j in range(len(df)):
        df.loc[j,'Date'] = datetime.strptime(str(df.loc[j,'Date']), "%Y%m")
        # df.loc[j,'Month'] = df.loc[j,'Date'].month()

    df = df[(df['month']==1) | (df['month']==1) | (df['month']==12)]


    df['Date'] = pd.to_datetime(df['Date'])
    x=df['Date']
    y=df['Converted']
    X=np.array(df.index)
    Y=np.array(df['Converted'])
    slope, intercept, r, p, se = linregress(X,Y)

    ax[i].plot(x,y)
    ax[i].plot(x,slope*X+intercept,'k--')
    ax[i].set_xlabel('p-value={:.3f}   R\u00b2={:.2f}   slope={:.3f}'.format(p,r,slope))
    ax[i].set_ylabel(names[i]+' '+units[i])


plt.tight_layout()
# plt.show()
plt.savefig(dir+'\\Arkansas Trends/Statewide Trends.png')