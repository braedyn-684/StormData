import pandas as pd
import os

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\US Census/2010 Income before.csv')

df = df.drop(df.filter(like='!!Margin of Error').columns, axis=1)
df = df.drop(df.filter(like='!!Families').columns, axis=1)
df = df.drop(df.filter(like='!!Married-couple families').columns, axis=1)
df = df.drop(df.filter(like='!!Nonfamily households').columns, axis=1)
df = df[df['Label (Grouping)'] == "Median income (dollars)"]

# df = df.rename(columns={'Label (Grouping)':'COUNTY'})
df = df.set_index('Label (Grouping)')
df.columns = df.columns.str.replace('!!Households!!Estimate', '', regex=False)
df.to_csv(dir+'\\US Census/2010 Income.csv', index=True)



dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\US Census/2020 Income before.csv')

df = df.drop(df.filter(like='!!Margin of Error').columns, axis=1)
df = df.drop(df.filter(like='!!Families').columns, axis=1)
df = df.drop(df.filter(like='!!Married-couple families').columns, axis=1)
df = df.drop(df.filter(like='!!Nonfamily households').columns, axis=1)
df = df[df['Label (Grouping)'] == "Median income (dollars)"]
# df = df.rename(columns={'Label (Grouping)':'COUNTY'})
df = df.set_index('Label (Grouping)')
df.columns = df.columns.str.replace('!!Households!!Estimate', '', regex=False)
df.to_csv(dir+'\\US Census/2020 Income.csv', index=True)


dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\US Census/2000 Income before.csv')
# df = df.rename(columns={'Label (Grouping)':'COUNTY'})
df = df.set_index('Label (Grouping)')
df = df.drop(df.filter(like='!!Percent').columns, axis=1)
df = df.filter(like='!!Total population', axis=1)

df = df.loc[df.index == "        Median household income (dollars)"]
df.rename(index={'        Median household income (dollars)':'Median income (dollars)'}, inplace=True)
df.columns = df.columns.str.replace('!!Total population!!Number', '', regex=False)
df.to_csv(dir+'\\US Census/2000 Income.csv', index=True)