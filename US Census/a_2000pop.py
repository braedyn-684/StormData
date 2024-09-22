import pandas as pd
import os

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\2000 Population and Race before.csv')

df = df.drop(df.filter(like='!!Percent').columns, axis=1)
df = df[df['Label (Grouping)'] == 'Total population']

df.columns = df.columns.str.split('!!', expand=True)

df_transposed = df.T.reset_index()
df_transposed.columns = ['County', 'Label (Grouping)', 'Type','Value']
df_pivot = df_transposed.pivot(index='Label (Grouping)', columns='County', values='Value')

df_pivot.rename(index={'Black or African American alone':'        Black or African American alone'}, inplace=True)
df_pivot.rename(index={'American Indian and Alaska Native alone (300, A01-Z99)':'        American Indian and Alaska Native alone'}, inplace=True)
df_pivot.rename(index={'Asian alone (400-499)':'        Asian alone'}, inplace=True)
df_pivot.rename(index={'Native Hawaiian and Other Pacific Islander alone (500-599)':'        Native Hawaiian and Other Pacific Islander alone'}, inplace=True)
df_pivot.rename(index={'Some other race alone':'        Some Other Race alone'}, inplace=True)
df_pivot.rename(index={'Two or more races':'    Population of two or more races:'}, inplace=True)
df_pivot.rename(index={'Total population':'Total:'}, inplace=True)

df_pivot = df_pivot.drop(columns=['Label (Grouping)'])

df_pivot.to_csv(dir+'\\2000 Population and Race.csv')