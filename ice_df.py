import pandas as pd
import os
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df0 = pd.read_csv(dir+'\\Storm Data CPI.csv')
# ice_df = df0[df0['EVENT_TYPE']=="Ice Storm"]
# ice_df = ice_df.reset_index()
# file_save_name = 'master_ice'
event_types = ["Heavy Snow", "Winter Storm", "Winter Weather", "Ice Storm"]
ice_df = df0[df0['EVENT_TYPE'].isin(event_types)]
file_save_name = 'master'

df2 = pd.read_csv(dir+'\\Storm Data by County.csv')
county_names = df2['COUNTY']
FIPS = df2['FIPS']
df2 = df2.set_index('COUNTY')

#------------------------------CPI adjustments----------------------------------------#

ice_df['BEGIN_DATE_TIME'] = pd.to_datetime(ice_df['BEGIN_DATE_TIME'])
ice_df['END_DATE_TIME'] = pd.to_datetime(ice_df['END_DATE_TIME'])   
ice_df['HOURS'] = (ice_df['END_DATE_TIME'] - ice_df['BEGIN_DATE_TIME']).dt.total_seconds() / 3600
        
#----------------------------------Decadal groupings----------------------------#

ice_df.rename(columns={'CZ_NAME': 'COUNTY',
                       'DAMAGE_PROPERTY':'DMG',
                       'DAMAGE_PROPERTY_CPI':'DMGCPI',
                       'INJURIES_DIRECT': 'DIRINJ',
                       'INJURIES_INDIRECT':'INDINJ',
                       'DEATHS_DIRECT':'DIRDTH',
                       'DEATHS_INDIRECT':'INDDTH',
                       'CZ_FIPS':'FIPS'}, inplace=True)

ice_df['TOTINJ'] = ice_df['DIRINJ'] + ice_df['INDINJ']
ice_df['TOTDTH'] = ice_df['DIRDTH'] + ice_df['INDDTH']

dates = [datetime(1995,6,30), datetime(2005,6,30), datetime(2015,6,30), datetime(2025,6,30)]
date_name = ['2000','2010','2020']

def decades(input_df,date1,date2):
    new_df = input_df[(input_df['BEGIN_DATE_TIME']>=date1) & \
                    (input_df['BEGIN_DATE_TIME']<date2)]
    result = (new_df.groupby(['COUNTY', 'EVENT_TYPE']).size().unstack(fill_value=0).reset_index())
    result = result.set_index('COUNTY')


    # input_count = new_df['COUNTY'].value_counts().sort_index()
    # input_count_df = input_count.reset_index()
    # input_count_df.columns = ['COUNTY', 'Report_Count']
    new_df1 = new_df.groupby('COUNTY').agg({
        'FIPS': 'first',
        'DMG': 'sum',
        'DMGCPI': 'sum',
        'TOTINJ': 'sum',
        'TOTDTH': 'sum',
        'HOURS': 'sum'
     }).reset_index()
    new_df1 = new_df1.sort_values(by='COUNTY')

    counties = new_df1['COUNTY']
    new_df1 = new_df1.set_index('COUNTY')
    for county in counties:
        new_df1.loc[county,'HS'] = result.loc[county,'Heavy Snow']
        new_df1.loc[county,'WS'] = result.loc[county,'Winter Storm']
        new_df1.loc[county,'WW'] = result.loc[county,'Winter Weather']
        new_df1.loc[county,'IS'] = result.loc[county,'Ice Storm']
        new_df1.loc[county,'COUNT'] = new_df1.loc[county,'HS'] + new_df1.loc[county,'WS'] +\
              new_df1.loc[county,'WW'] + new_df1.loc[county,'IS']
    return new_df1
ice_df2000 = decades(ice_df,dates[0],dates[1])
ice_df2010 = decades(ice_df,dates[1],dates[2])
ice_df2020 = decades(ice_df,dates[2],dates[3])
ice_dfall = decades(ice_df,dates[0],dates[3])

#----------------------------COUNTY NAMES-----------------------------------#
df = ice_dfall[['FIPS','DMG','DMGCPI','HS','WS','WW','IS','COUNT']]
# df = df.set_index('COUNTY')
df = df.sort_index()

#----------------------------US CENSUS--------------------------------------#
demo = pd.read_csv(dir+'\\US Census/Decadal Demographic info.csv')
for i in range(len(demo)):
    demo.loc[i,'COUNTY'] = demo.loc[i,'COUNTY'].upper()
demo = demo.set_index('COUNTY')
demo = demo.sort_index()

#------------------------------LULC-----------------------------------------#
lulc2001 = pd.read_csv(dir+'\\Land Cover\\Arkansas_LandCover_Percents_01.csv')
for i in range(len(lulc2001)):
    lulc2001.loc[i,'COUNTY'] = lulc2001.loc[i,'COUNTY'].upper()
lulc2001 = lulc2001.set_index('COUNTY')
lulc2001 = lulc2001.sort_index()

lulc2011 = pd.read_csv(dir+'\\Land Cover\\Arkansas_LandCover_Percents_11.csv')
for i in range(len(lulc2011)):
    lulc2011.loc[i,'COUNTY'] = lulc2011.loc[i,'COUNTY'].upper()
lulc2011 = lulc2011.set_index('COUNTY')
lulc2011 = lulc2011.sort_index()

lulc2021 = pd.read_csv(dir+'\\Land Cover\\Arkansas_LandCover_Percents_21.csv')
for i in range(len(lulc2021)):
    lulc2021.loc[i,'COUNTY'] = lulc2021.loc[i,'COUNTY'].upper()
lulc2021 = lulc2021.set_index('COUNTY')
lulc2021 = lulc2021.sort_index()

#------------------------------ELEVATION------------------------------------#
elev = pd.read_csv(dir+'\\Land Cover\\Arkansas_Mean_Elevation.csv')
for i in range(len(elev)):
    elev.loc[i,'COUNTY'] = elev.loc[i,'NAME'].upper()
elev = elev.set_index('COUNTY')
elev = elev.sort_index()

#---------------------------------WEATHER-----------------------------------#
mtmp = pd.read_csv(dir+'\\Precip and Temp\\Arkansas_Monthly_Mean_Temps_and_Precip_and_Snow_by_County.csv')
for i in range(len(mtmp)):
    mtmp.loc[i,'COUNTY'] = mtmp.loc[i,'county_name'].upper()
mtmp = mtmp.set_index('COUNTY')
mtmp = mtmp.sort_index()

#------------------------------main csv-------------------------------------#
for county in county_names:
    df.loc[county,'County_low'] = mtmp.loc[county,'county_name']
    df.loc[county,'DMG'] = ice_dfall.loc[county,'DMG']
    df.loc[county,'INJ'] = ice_dfall.loc[county,'TOTINJ']
    df.loc[county,'DTH'] = ice_dfall.loc[county,'TOTDTH']
    df.loc[county,'HS'] = ice_dfall.loc[county,'HS']
    df.loc[county,'WS'] = ice_dfall.loc[county,'WS']
    df.loc[county,'WW'] = ice_dfall.loc[county,'WW']
    df.loc[county,'IS'] = ice_dfall.loc[county,'IS']
    df.loc[county,'HOURS'] = ice_dfall.loc[county,'HOURS']
    df.loc[county,'COUNT'] = ice_dfall.loc[county,'COUNT']
    df.loc[county,'INJ2000'] = ice_df2000.loc[county,'TOTINJ']
    df.loc[county,'DTH2000'] = ice_df2000.loc[county,'TOTDTH']
    df.loc[county,'INJ2010'] = ice_df2010.loc[county,'TOTINJ']
    df.loc[county,'DTH2010'] = ice_df2010.loc[county,'TOTDTH']
    df.loc[county,'INJ2020'] = ice_df2020.loc[county,'TOTINJ']
    df.loc[county,'DTH2020'] = ice_df2020.loc[county,'TOTDTH']
    df.loc[county,'DMG2000'] = ice_df2000.loc[county,'DMG']
    df.loc[county,'DMGCP2000'] = ice_df2000.loc[county,'DMGCPI']
    df.loc[county,'COUNT2000'] = ice_df2000.loc[county,'COUNT']
    df.loc[county,'HS2000'] = ice_df2000.loc[county,'HS']
    df.loc[county,'WS2000'] = ice_df2000.loc[county,'WS']
    df.loc[county,'WW2000'] = ice_df2000.loc[county,'WW']
    df.loc[county,'IS2000'] = ice_df2000.loc[county,'IS']
    df.loc[county,'HOURS00'] = ice_df2000.loc[county,'HOURS']
    df.loc[county,'DMG2010'] = ice_df2010.loc[county,'DMG']
    df.loc[county,'DMGCP2010'] = ice_df2010.loc[county,'DMGCPI']
    df.loc[county,'COUNT2010'] = ice_df2010.loc[county,'COUNT']
    df.loc[county,'HS2010'] = ice_df2010.loc[county,'HS']
    df.loc[county,'WS2010'] = ice_df2010.loc[county,'WS']
    df.loc[county,'WW2010'] = ice_df2010.loc[county,'WW']
    df.loc[county,'IS2010'] = ice_df2010.loc[county,'IS']
    df.loc[county,'HOURS10'] = ice_df2010.loc[county,'HOURS']
    df.loc[county,'DMG2020'] = ice_df2020.loc[county,'DMG']
    df.loc[county,'DMGCP2020'] = ice_df2020.loc[county,'DMGCPI']
    df.loc[county,'COUNT2020'] = ice_df2020.loc[county,'COUNT']
    df.loc[county,'HS2020'] = ice_df2020.loc[county,'HS']
    df.loc[county,'WS2020'] = ice_df2020.loc[county,'WS']
    df.loc[county,'WW2020'] = ice_df2020.loc[county,'WW']
    df.loc[county,'IS2020'] = ice_df2020.loc[county,'IS']
    df.loc[county,'HOURS20'] = ice_df2020.loc[county,'HOURS']
    df.loc[county,'POP2000'] = demo.loc[county,'POP2000']
    df.loc[county,'PNW2000'] = demo.loc[county,'PNW2000']
    df.loc[county,'MICPI2000'] = demo.loc[county,'MICPI2000']
    df.loc[county,'MGRCP2000'] = demo.loc[county,'MGRCP2000']
    df.loc[county,'POP2010'] = demo.loc[county,'POP2010']
    df.loc[county,'PNW2010'] = demo.loc[county,'PNW2010']
    df.loc[county,'MICPI2010'] = demo.loc[county,'MICPI2010']
    df.loc[county,'MGRCP2010'] = demo.loc[county,'MGRCP2010']
    df.loc[county,'POP2020'] = demo.loc[county,'POP2020']
    df.loc[county,'PNW2020'] = demo.loc[county,'PNW2020']
    df.loc[county,'MICPI2020'] = demo.loc[county,'MICPI2020']
    df.loc[county,'MGRCP2020'] = demo.loc[county,'MGRCP2020']
    df.loc[county,'AG01'] = lulc2001.loc[county,'AG01']
    df.loc[county,'FOR01'] = lulc2001.loc[county,'FOR01']
    df.loc[county,'URB01'] = lulc2001.loc[county,'URB01']
    df.loc[county,'WAT01'] = lulc2001.loc[county,'WAT01']
    df.loc[county,'AG11'] = lulc2011.loc[county,'AG11']
    df.loc[county,'FOR11'] = lulc2011.loc[county,'FOR11']
    df.loc[county,'URB11'] = lulc2011.loc[county,'URB11']
    df.loc[county,'WAT11'] = lulc2011.loc[county,'WAT11']
    df.loc[county,'AG21'] = lulc2021.loc[county,'AG21']
    df.loc[county,'FOR21'] = lulc2021.loc[county,'FOR21']
    df.loc[county,'URB21'] = lulc2021.loc[county,'URB21']
    df.loc[county,'WAT21'] = lulc2021.loc[county,'WAT21']
    df.loc[county,'ELEV'] = elev.loc[county,'mean']
    df.loc[county,'TMP2000'] = mtmp.loc[county,'mean temp (2000)']
    df.loc[county,'PCP2000'] = mtmp.loc[county,'mean precip (2000)']
    df.loc[county,'SNW2000'] = mtmp.loc[county,'mean snow (2000)']
    df.loc[county,'TMP2010'] = mtmp.loc[county,'mean temp (2010)']
    df.loc[county,'PCP2010'] = mtmp.loc[county,'mean precip (2010)']
    df.loc[county,'SNW2010'] = mtmp.loc[county,'mean snow (2010)']
    df.loc[county,'TMP2020'] = mtmp.loc[county,'mean temp (2020)']
    df.loc[county,'PCP2020'] = mtmp.loc[county,'mean precip (2020)']
    df.loc[county,'SNW2020'] = mtmp.loc[county,'mean snow (2020)']

df['DMGPOP2000'] = df['DMGCP2000'] / df['POP2000']  
df['DMGPOP2010'] = df['DMGCP2010'] / df['POP2010']  
df['DMGPOP2020'] = df['DMGCP2020'] / df['POP2020']  

df['DPC2000'] = df['DMGPOP2000'] / df['COUNT2000']
df['DPC2010'] = df['DMGPOP2010'] / df['COUNT2010']
df['DPC2020'] = df['DMGPOP2020'] / df['COUNT2020']

# for county in county_names:
#     if pd.isna(new_df1.loc[county, 'COUNT']):
#             new_df1.loc[county, 'COUNT'] = 0

df.to_csv(dir+'\\'+file_save_name+'.csv',index=True)

cols = ['DMG', 'DMGCPI', 
       'DMG2000', 'DMGCP2000', 'COUNT2000', 'HS2000','WS2000','WW2000','IS2000', 'HOURS00',
       'DMG2010', 'DMGCP2010', 'COUNT2010', 'HS2010','WS2010','WW2010','IS2010', 'HOURS10',
       'DMG2020', 'DMGCP2020','COUNT2020', 'HS2020','WS2020','WW2020','IS2020', 'HOURS20',
       'POP2000', 'PNW2000', 'MICPI2000', 'MGRCP2000', 
       'POP2010', 'PNW2010','MICPI2010', 'MGRCP2010', 
       'POP2020', 'PNW2020', 'MICPI2020', 'MGRCP2020', 
       'AG01', 'FOR01','URB01', 'WAT01', 'AG11', 'FOR11','URB11', 'WAT11', 'AG21', 'FOR21','URB21', 'WAT21', 
       'ELEV', 'TMP2000', 'PCP2000', 'SNW2000', 'TMP2010', 'PCP2010',
       'SNW2010','TMP2020', 'PCP2020','SNW2020','DMGPOP2000', 'DMGPOP2010', 'DMGPOP2020',
       'DPC2000', 'DPC2010', 'DPC2020']
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[cols])
scaled_df = pd.DataFrame(scaled_data, columns=cols, index=df.index)

for county in county_names:
    scaled_df.loc[county,'FIPS'] = df.loc[county,'FIPS']
    scaled_df.loc[county,'County_low'] = df.loc[county,'County_low']

scaled_df.to_csv(dir+'\\'+file_save_name+'_scaled.csv',index=True)