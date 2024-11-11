import pandas as pd
import os 
from datetime import datetime


dates = [datetime(2009,1,25), datetime(2009,1,29)]
file_save_name = 'jan2009'


dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

df2 = pd.read_csv(dir+'\\Storm Data by County.csv')
county_names = df2['COUNTY']
FIPS = df2['FIPS']
df2 = df2.set_index('COUNTY')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['END_DATE_TIME'] = pd.to_datetime(df['END_DATE_TIME'])

df.rename(columns={'CZ_NAME': 'COUNTY',
                       'DAMAGE_PROPERTY':'DMG',
                       'DAMAGE_PROPERTY_CPI':'DMGCPI',
                       'CZ_FIPS':'FIPS'}, inplace=True)

def decades(input_df,date1,date2):
    new_df = input_df[(input_df['BEGIN_DATE_TIME']>=date1) & \
                    (input_df['BEGIN_DATE_TIME']<date2)]
    new_df1 = new_df.groupby('COUNTY').agg({
        'FIPS': 'first',
        'DMG': 'sum',
        'DMGCPI': 'sum',
     }).reset_index()
    new_df1 = new_df1.sort_values(by='COUNTY')
    counties = new_df1['COUNTY']
    new_df1 = new_df1.set_index('COUNTY')
    for county in counties:
        new_df1.loc[county,'FIPS'] = df2.loc[county,'FIPS']
    return new_df1

case_study = decades(df,dates[0],dates[1])

#----------------------------US CENSUS--------------------------------------#
demo = pd.read_csv(dir+'\\US Census/Decadal Demographic info.csv')
for i in range(len(demo)):
    demo.loc[i,'COUNTY'] = demo.loc[i,'COUNTY'].upper()
demo = demo.set_index('COUNTY')
demo = demo.sort_index()

#------------------------------LULC-----------------------------------------#
lulc = pd.read_csv(dir+'\\Arkansas_LandCover_Percents.csv')
for i in range(len(lulc)):
    lulc.loc[i,'COUNTY'] = lulc.loc[i,'COUNTY'].upper()
lulc = lulc.set_index('COUNTY')
lulc = lulc.sort_index()

#------------------------------ELEVATION------------------------------------#
elev = pd.read_csv(dir+'\\Arkansas_Mean_Elevation.csv')
for i in range(len(elev)):
    elev.loc[i,'COUNTY'] = elev.loc[i,'NAME'].upper()
elev = elev.set_index('COUNTY')
elev = elev.sort_index()

#---------------------------------WEATHER-----------------------------------#
mtmp = pd.read_csv(dir+'\\Arkansas_Monthly_Mean_Temps_and_Precip_by_County.csv')
for i in range(len(mtmp)):
    mtmp.loc[i,'COUNTY'] = mtmp.loc[i,'county_name'].upper()
mtmp = mtmp.set_index('COUNTY')
mtmp = mtmp.sort_index()

#---------------------------------MAIN CSV BASE-----------------------------------#
df = case_study

#------------------------------add to main csv-------------------------------------#
county_names = case_study.index
for county in county_names:
    df.loc[county,'County_low'] = mtmp.loc[county,'county_name']
    df.loc[county,'POP2010'] = demo.loc[county,'POP2010']
    df.loc[county,'PNW2010'] = demo.loc[county,'PNW2010']
    df.loc[county,'MICPI2010'] = demo.loc[county,'MICPI2010']
    df.loc[county,'MGRCP2010'] = demo.loc[county,'MGRCP2010']
    df.loc[county,'AGPER'] = lulc.loc[county,'AGPER']
    df.loc[county,'FORPER'] = lulc.loc[county,'FORPER']
    df.loc[county,'URBPER'] = lulc.loc[county,'URBPER']
    df.loc[county,'WATPER'] = lulc.loc[county,'WATPER']
    df.loc[county,'ELEV'] = elev.loc[county,'mean']
    df.loc[county,'TMP2010'] = mtmp.loc[county,'mean temp (2010)']
    df.loc[county,'PCP2010'] = mtmp.loc[county,'mean precip (2010)']

df['DMGPOP2010'] = df['DMG'] / df['POP2010']   

df.to_csv(dir+'\\Case_Study_Jan_2009\\'+file_save_name+'.csv',index=True)

cols = ['DMG', 'DMGCPI', 'POP2010', 'PNW2010',
       'MICPI2010', 'MGRCP2010', 'AGPER', 'FORPER',
       'URBPER', 'WATPER', 'ELEV', 'TMP2010', 'PCP2010',
       'DMGPOP2010']
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[cols])
scaled_df = pd.DataFrame(scaled_data, columns=cols, index=df.index)

for county in county_names:
    scaled_df.loc[county,'FIPS'] = df.loc[county,'FIPS']
    scaled_df.loc[county,'County_low'] = df.loc[county,'County_low']

scaled_df.to_csv(dir+'\\Case_Study_Jan_2009\\'+file_save_name+'_scaled.csv',index=True)