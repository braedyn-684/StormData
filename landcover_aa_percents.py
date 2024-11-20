import pandas as pd
import os

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Arkansas_LandCover_Total.csv')
county_names = df['County']

columns = [           
    'Open water',         # 11
    'Developed, open',    # 21
    'Developed, low',     # 22
    'Developed, medium',  # 23
    'Developed, high',    # 24
    'Barren land',        # 31
    'Deciduous forest',   # 41
    'Evergreen forest',   # 42
    'Mixed forest',       # 43
    'Shrub/scrub',        # 52
    'Grassland/herbaceous',# 71
    'Pasture/hay',        # 81
    'Cultivated crops',   # 82
    'Woody wetlands',     # 90
    'Emergent herbaceous wetlands' # 95
]

column_order = ['County'] + columns
df = df[column_order]
# print(df.head())

df['Total'] = df.iloc[0:, 1:].sum(axis=1)
counties = df['County']
df = df.rename(columns={'County':'COUNTY'})
df = df.set_index('COUNTY')

df1 = pd.DataFrame(columns=columns, index=df.index)
for county in counties:
    for column in columns:
        df1.loc[county, columns] = (df.loc[county, columns]/df.loc[county,'Total'])*100

COLS = ['Ag','AGPER','For','FORPER','Urb','URBPER','Wat','WATPER','Total']
df2 = pd.DataFrame(columns=COLS, index=df.index)
df2['Total'] = df['Total']
df2['Ag'] = df['Pasture/hay']+df['Cultivated crops']
df2['For'] = df['Deciduous forest']# +df['Evergreen forest']+df['Mixed forest']
df2['Urb'] = df['Developed, open']+df['Developed, low']+df['Developed, medium']+df['Developed, high']
df2['Wat'] = df['Open water']

df2['AGPER'] =  (df2['Ag'] /df['Total'])*100
df2['FORPER'] = (df2['For']/df['Total'])*100
df2['URBPER'] = (df2['Urb']/df['Total'])*100
df2['WATPER'] = (df2['Wat']/df['Total'])*100

df2.to_csv(dir+'\\Land Cover\\Arkansas_LandCover_Percents.csv')