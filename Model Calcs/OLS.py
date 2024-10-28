import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\master.csv')

Y = df['DMGCP2010']
X = df[['POP2010','PNW2010','MICPI2010','AGPER','URBPER','WATPER','ELEV','TMP2010','PCP2010']]
# X = df[['ELEV','TMP2000']]

X = sm.add_constant(X)
model = sm.OLS(Y,X).fit()
print(model.summary())