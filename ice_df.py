import pandas as pd
import os
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df0 = pd.read_csv(dir+'\\Storm Data CPI.csv')
ice_df = df0[df0['EVENT_TYPE']=="Ice Storm"]
ice_df = ice_df.reset_index()
file_save_name = 'master ice'
# event_types = ["Heavy Snow", "Winter Storm", "Winter Weather", "Ice Storm"]
# ice_df = df0[df0['EVENT_TYPE'].isin(event_types)]
# file_save_name = 'master'

df2 = pd.read_csv(dir+'\\Storm Data by County.csv')
county_names = df2['COUNTY']
FIPS = df2['FIPS']
df2 = df2.set_index('COUNTY')

#------------------------------CPI adjustments----------------------------------------#

ice_df['BEGIN_DATE_TIME'] = pd.to_datetime(ice_df['BEGIN_DATE_TIME'])
ice_df['END_DATE_TIME'] = pd.to_datetime(ice_df['END_DATE_TIME'])   
        
#----------------------------------Decadal groupings----------------------------#

ice_df.rename(columns={'CZ_NAME': 'COUNTY',
                       'DAMAGE_PROPERTY':'DMG',
                       'DAMAGE_PROPERTY_CPI':'DMGCPI',
                       'CZ_FIPS':'FIPS'}, inplace=True)
dates = [datetime(1995,6,30), datetime(2005,6,30), datetime(2015,6,30), datetime(2025,6,30)]
date_name = ['2000','2010','2020']

def decades(input_df,date1,date2):
    new_df = input_df[(input_df['BEGIN_DATE_TIME']>=date1) & \
                    (input_df['BEGIN_DATE_TIME']<date2)]
    input_count = new_df['COUNTY'].value_counts().sort_index()
    input_count_df = input_count.reset_index()
    input_count_df.columns = ['COUNTY', 'Report_Count']
    new_df1 = new_df.groupby('COUNTY').agg({
        'FIPS': 'first',
        'DMG': 'sum',
        'DMGCPI': 'sum',
     }).reset_index()
    new_df1 = new_df1.sort_values(by='COUNTY')
    counties = new_df1['COUNTY']
    new_df1 = new_df1.set_index('COUNTY')
    new_df1 = new_df1.reindex(county_names, fill_value=0).reset_index()
    input_count_df = input_count_df.set_index('COUNTY')
    new_df1 = new_df1.set_index('COUNTY')
    for county in counties:
        new_df1.loc[county,'COUNT'] = input_count_df.loc[county,'Report_Count']
        new_df1.loc[county,'FIPS'] = df2.loc[county,'FIPS']
    return new_df1
ice_df2000 = decades(ice_df,dates[0],dates[1])
ice_df2010 = decades(ice_df,dates[1],dates[2])
ice_df2020 = decades(ice_df,dates[2],dates[3])
ice_dfall = decades(ice_df,dates[0],dates[3])

#----------------------------COUNTY NAMES-----------------------------------#
df = ice_dfall[['FIPS','DMG','DMGCPI']]
# df = df.set_index('COUNTY')
df = df.sort_index()

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

#------------------------------main csv-------------------------------------#
for county in county_names:
    df.loc[county,'County'] = mtmp.loc[county,'county_name']
    df.loc[county,'DMG2000'] = ice_df2000.loc[county,'DMG']
    df.loc[county,'DMGCP2000'] = ice_df2000.loc[county,'DMGCPI']
    df.loc[county,'COUNT2000'] = ice_df2000.loc[county,'COUNT']
    df.loc[county,'DMG2010'] = ice_df2010.loc[county,'DMG']
    df.loc[county,'DMGCP2010'] = ice_df2010.loc[county,'DMGCPI']
    df.loc[county,'COUNT2010'] = ice_df2010.loc[county,'COUNT']
    df.loc[county,'DMG2020'] = ice_df2020.loc[county,'DMG']
    df.loc[county,'DMGCP2020'] = ice_df2020.loc[county,'DMGCPI']
    df.loc[county,'COUNT2020'] = ice_df2020.loc[county,'COUNT']
    df.loc[county,'POP2000'] = demo.loc[county,'POP2000']
    df.loc[county,'PNW2000'] = demo.loc[county,'PNW2000']
    df.loc[county,'MICPI2000'] = demo.loc[county,'MICPI2000']
    df.loc[county,'POP2010'] = demo.loc[county,'POP2010']
    df.loc[county,'PNW2010'] = demo.loc[county,'PNW2010']
    df.loc[county,'MICPI2010'] = demo.loc[county,'MICPI2010']
    df.loc[county,'POP2020'] = demo.loc[county,'POP2020']
    df.loc[county,'PNW2020'] = demo.loc[county,'PNW2020']
    df.loc[county,'MICPI2020'] = demo.loc[county,'MICPI2020']
    df.loc[county,'AGPER'] = lulc.loc[county,'AGPER']
    df.loc[county,'FORPER'] = lulc.loc[county,'FORPER']
    df.loc[county,'URBPER'] = lulc.loc[county,'URBPER']
    df.loc[county,'WATPER'] = lulc.loc[county,'WATPER']
    df.loc[county,'ELEV'] = elev.loc[county,'mean']
    df.loc[county,'TMP2000'] = mtmp.loc[county,'mean temp (2000)']
    df.loc[county,'PCP2000'] = mtmp.loc[county,'mean precip (2000)']
    df.loc[county,'TMP2010'] = mtmp.loc[county,'mean temp (2010)']
    df.loc[county,'PCP2010'] = mtmp.loc[county,'mean precip (2010)']
    df.loc[county,'TMP2020'] = mtmp.loc[county,'mean temp (2020)']
    df.loc[county,'PCP2020'] = mtmp.loc[county,'mean precip (2020)']

df['DMGPOP2000'] = df['DMGCP2000'] / df['POP2000']  
df['DMGPOP2010'] = df['DMGCP2010'] / df['POP2000']  
df['DMGPOP2020'] = df['DMGCP2020'] / df['POP2020']  

df['DPC2000'] = df['DMGPOP2000'] / df['COUNT2000']
df['DPC2010'] = df['DMGPOP2010'] / df['COUNT2010']
df['DPC2020'] = df['DMGPOP2020'] / df['COUNT2020']

df.to_csv(dir+'\\'+file_save_name+'.csv',index=True)

cols = ['DMG', 'DMGCPI', 'DMG2000', 'DMGCP2000', 'COUNT2000',
       'DMG2010', 'DMGCP2010', 'COUNT2010', 'DMG2020', 'DMGCP2020',
       'COUNT2020', 'POP2000', 'PNW2000', 'MICPI2000', 'POP2010', 'PNW2010',
       'MICPI2010', 'POP2020', 'PNW2020', 'MICPI2020', 'AGPER', 'FORPER',
       'URBPER', 'WATPER', 'ELEV', 'TMP2000', 'PCP2000', 'TMP2010', 'PCP2010',
       'TMP2020', 'PCP2020', 'DMGPOP2000', 'DMGPOP2010', 'DMGPOP2020',
       'DPC2000', 'DPC2010', 'DPC2020']
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[cols])
scaled_df = pd.DataFrame(scaled_data, columns=cols, index=df.index)

for county in county_names:
    scaled_df.loc[county,'FIPS'] = df.loc[county,'FIPS']
    scaled_df.loc[county,'County'] = df.loc[county,'County']

scaled_df.to_csv(dir+'\\'+file_save_name+'_scaled.csv',index=True)