import pandas as pd
import os


year = '2000'
dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\US Census\\'+year+' Median Gross Rent.csv')

if year != '2000':
    for i in range(len(df)):
        if pd.isna(df.iloc[i,1]) and "    Estimate" in str(df.iloc[i+1,0]):
            df.loc[i,"Median gross rent"] = df.loc[i+1,"Median gross rent"]
    df = df[~df.iloc[:, 0].str.contains("    Estimate", na=False)]
else:
    for i in range(len(df)):
        if pd.isna(df.iloc[i,1]) and "    " in str(df.iloc[i+1,0]):
            df.loc[i,"Median gross rent"] = df.loc[i+1,"Median gross rent"]
    df = df[~df.iloc[:, 0].str.contains("    ", na=False)]


df.reset_index(drop=True, inplace=True)

df.iloc[:, 0] = df.iloc[:, 0].str.replace(" County, Arkansas", "", regex=False)

df = df.set_index('Label (Grouping)')
df.index.name = 'COUNTY'

df.to_csv(dir+'\\US Census\\'+year+' Median Gross Rent fixed.csv')