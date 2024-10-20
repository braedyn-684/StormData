import pandas as pd
import numpy as np
import os
from scipy.stats import linregress
dir = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(dir+'\\master.csv')
county_names = df['COUNTY']

index_labels = ['slope', 'intercept', 'r-squared', 'p-value', 'standard error']
df1 = pd.DataFrame(index=index_labels)


environmental = ['AGPER', 'FORPER', 'URBPER', 'WATPER', 'ELEV']
dependents = ['DMGCP','INJ','DTH']
for item in environmental:
    for dependent in dependents:
        x = dependent
        y = item
        DMG = np.array(df[x])
        VAR = np.array(df[y])

        slope, intercept, r, p, se = linregress(DMG, VAR)
        df1.loc['slope',x+'_'+y] = slope
        df1.loc['intercept',x+'_'+y] = intercept
        df1.loc['r-squared',x+'_'+y] = r**2
        df1.loc['p-value',x+'_'+y] = p
        df1.loc['standard error',x+'_'+y] = se

demographic = ['POP','PNW','MICPI']
years = ['2000','2010','2020']
for item in demographic:
    for year in years:
        for dependent in dependents:
            x = dependent+year
            y = item+year
            DMG = np.array(df[x])
            VAR = np.array(df[y])

            slope, intercept, r, p, se = linregress(DMG, VAR)
            df1.loc['slope',x+'_'+y] = slope
            df1.loc['intercept',x+'_'+y] = intercept
            df1.loc['r-squared',x+'_'+y] = r**2
            df1.loc['p-value',x+'_'+y] = p
            df1.loc['standard error',x+'_'+y] = se
for year in years:
    x = 'MINC'+year
    y = 'DMG'+year
    DMG = np.array(df[x])
    VAR = np.array(df[y])

    slope, intercept, r, p, se = linregress(DMG, VAR)
    df1.loc['slope',x+'_'+y] = slope
    df1.loc['intercept',x+'_'+y] = intercept
    df1.loc['r-squared',x+'_'+y] = r**2
    df1.loc['p-value',x+'_'+y] = p
    df1.loc['standard error',x+'_'+y] = se

df1 = df1.T
df1.to_csv(dir+'\\Correlation Plots\\correlation.csv')