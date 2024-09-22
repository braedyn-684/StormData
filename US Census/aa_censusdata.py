import pandas as pd
import os

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\2020 Population and Race.csv')
df = df.set_index('Label (Grouping)')
county_names = df.columns.str.replace(" County, Arkansas", "")
df_ = pd.DataFrame(index=county_names)

years = ['2000','2010','2020']
for i in range(len(years)):
    df = pd.read_csv(dir+'\\'+years[i]+' Population and Race.csv')

    df = df.set_index('Label (Grouping)')

    df.columns = df.columns.str.replace(" County, Arkansas", "")

    if i == 1:
       df.loc['Total:','Ouachita'] = '26,120'
       df.rename(index={'    Two or More Races:':'    Population of two or more races:'}, inplace=True)
    for col in df.columns:
        df[col] = df[col].str.replace(',', '').astype(float)
    df.fillna(0, inplace=True)

    for county in county_names:
        name = 'POP'+years[i]
        df_.loc[county,name] = df.loc['Total:',county]

    for county in county_names:

        non_white = df.loc['        Black or African American alone',county] +\
        df.loc['        American Indian and Alaska Native alone',county] +\
        df.loc['        Asian alone',county] +\
        df.loc['        Native Hawaiian and Other Pacific Islander alone',county] +\
        df.loc['        Some Other Race alone',county] +\
        df.loc['    Population of two or more races:',county]

        df_.loc[county,'PNW'+years[i]] = non_white * 100 / df_.loc[county,'POP'+years[i]]


for i in range(len(years)):
 if i ==1:
    df = pd.read_csv(dir+'\\'+years[i]+' Income.csv')
    df = df.set_index('Label (Grouping)')
    df.columns = df.columns.str.replace(" County, Arkansas", "")
    for col in df.columns:
        print(col)
        df[col] = df[col].str.replace(',', '').astype(float)

    for county in county_names:
        name = 'MINC'+years[i]
        df_.loc[county,name] = df.loc['Median income (dollars)',county]



    # df = pd.read_csv(dir+'\\'+years[i]+' Population and Race.csv')