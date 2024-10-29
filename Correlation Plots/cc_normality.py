import pandas as pd
import os
from scipy.stats import normaltest

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\master.csv')

print('Normal test for 2000, 2010, and 2020')
print('---------------------------------------------------')
first  = normaltest(df['DMGCP2000'])
print('stat: \t',round(first.statistic,4))
print('p-value:',round(first.pvalue,4))
second = normaltest(df['DMGCP2010'])
print('stat: \t',round(second.statistic,4))
print('p-value:',round(second.pvalue,4))
third = normaltest(df['DMGCP2020'])
print('stat: \t',round(third.statistic,4))
print('p-value:',round(third.pvalue,4))

