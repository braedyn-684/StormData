import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

counties = ['Craighead','Pulaski','Washington']

dir = os.path.dirname(os.path.abspath(__file__))

for i in range(3):
    fig, ax = plt.subplots(1,3, figsize=(16,6))
    fig.suptitle('Trends at '+counties[i]+' County from 1900-2024')

    df = pd.read_csv(dir+'\\Arkansas Trends/'+counties[i]+' County Precip.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    x=df['Date']
    y=df['Precip']
    X=np.array(df.index)
    Y=np.array(df['Precip'])
    slope, intercept, r, p, se = linregress(X,Y)

    ax[0].plot(x,y)
    ax[0].plot(x,slope*X+intercept,'k--')
    ax[0].set_xlabel('p-value={:.3f}   R2={:.1f}   slope={:.3f}'.format(p,r,slope))
    ax[0].set_ylabel('precipitation (in)')

    df = pd.read_csv(dir+'\\Arkansas Trends/'+counties[i]+' County Temps.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    x=df['Date']
    y=df['Tmin']
    X=np.array(df.index)
    Y=np.array(df['Tmin'])
    slope, intercept, r, p, se = linregress(X,Y)
    ax[1].plot(x,y)
    ax[1].plot(x,slope*X+intercept,'k--')
    ax[1].set_xlabel('p-value={:.3f}   R2={:.1f}   slope={:.3f}'.format(p,r,slope))
    ax[1].set_ylabel('min temperature (F)')

    y=df['Tmax']
    Y=np.array(df['Tmax'])
    slope, intercept, r, p, se = linregress(X,Y)
    ax[2].plot(x,y)
    ax[2].plot(x,slope*X+intercept,'k--')
    ax[2].set_xlabel('p-value={:.3f}   R2={:.1f}   slope={:.3f}'.format(p,r,slope))
    ax[2].set_ylabel('max temperature (F)')

    y=df['Tmax']
    Y=np.array(df['Tmax'])
    slope, intercept, r, p, se = linregress(X,Y)
    ax[2].plot(x,y)
    ax[2].plot(x,slope*X+intercept,'k--')
    ax[2].set_xlabel('p-value={:.3f}   R2={:.1f}   slope={:.3f}'.format(p,r,slope))
    ax[2].set_ylabel('max temperature (F)')

    plt.tight_layout()
    plt.savefig(dir+'\\Arkansas Trends/'+counties[i]+' Trends.png')