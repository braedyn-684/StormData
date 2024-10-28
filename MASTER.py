import pandas as pd
import os


dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data by County.csv')
county_names = df['COUNTY']
org2000 = pd.read_csv(dir+'\\Storm Data by County 2000.csv')
org2010 = pd.read_csv(dir+'\\Storm Data by County 2010.csv')
org2020 = pd.read_csv(dir+'\\Storm Data by County 2020.csv')

demo = pd.read_csv(dir+'\\US Census/Decadal Demographic info.csv')
for i in range(len(demo)):
    demo.loc[i,'COUNTY'] = demo.loc[i,'COUNTY'].upper()

lulc = pd.read_csv(dir+'\\Arkansas_LandCover_Percents.csv')
lulc = lulc.rename(columns={'NAME':'COUNTY'})
for i in range(len(lulc)):
    lulc.loc[i,'COUNTY'] = lulc.loc[i,'COUNTY'].upper()
lulc = lulc.set_index('COUNTY')
lulc = lulc.sort_index()

df = df[['COUNTY','FIPS','DMGPRP','DMGPRPCPI','TOTAL_INJURIES','TOTAL_DEATHS']].rename(columns={
    'COUNTY':'COUNTY',
    'FIPS':'FIPS',
    'DMGPRP':'DMG',
    'DMGPRPCPI':'DMGCP',
    'TOTAL_INJURIES':'INJ',
    'TOTAL_DEATHS':'DTH'
})

df = df.set_index('COUNTY')
org2000 = org2000.set_index('COUNTY')
org2010 = org2010.set_index('COUNTY')
org2020 = org2020.set_index('COUNTY')
demo = demo.set_index('COUNTY')
for county in county_names:
    df.loc[county,'DMGCP'] = round(df.loc[county,'DMGCP'],0)
    df.loc[county,'DMG2000'] = round(org2000.loc[county,'DMGPRP'],0)
    df.loc[county,'DMGCP2000'] = round(org2000.loc[county,'DMGPRPCPI'],0)
    df.loc[county,'INJ2000'] = org2000.loc[county,'TOTAL_INJURIES']
    df.loc[county,'DTH2000'] = org2000.loc[county,'TOTAL_DEATHS']
    df.loc[county,'DMG2010'] = round(org2010.loc[county,'DMGPRP'],0)
    df.loc[county,'DMGCP2010'] = round(org2010.loc[county,'DMGPRPCPI'],0)
    df.loc[county,'INJ2010'] = org2010.loc[county,'TOTAL_INJURIES']
    df.loc[county,'DTH2010'] = org2010.loc[county,'TOTAL_DEATHS']
    df.loc[county,'DMG2020'] = round(org2020.loc[county,'DMGPRP'],0)
    df.loc[county,'DMGCP2020'] = round(org2020.loc[county,'DMGPRPCPI'],0)
    df.loc[county,'INJ2020'] = org2020.loc[county,'TOTAL_INJURIES']
    df.loc[county,'DTH2020'] = org2020.loc[county,'TOTAL_DEATHS']

df = pd.merge(df,demo,left_index=True, right_index=True)

for county in county_names:
    df.loc[county,'AGPER'] = round(lulc.loc[county,'AGPER'],2)
    df.loc[county,'FORPER'] = round(lulc.loc[county,'FORPER'],2)
    df.loc[county,'URBPER'] = round(lulc.loc[county,'URBPER'],2)
    df.loc[county,'WATPER'] = round(lulc.loc[county,'WATPER'],2)

elev = pd.read_csv(dir+'\\Arkansas_Mean_Elevation.csv')
for i in range(len(elev)):
    elev.loc[i,'NAME'] = elev.loc[i,'NAME'].upper()
elev = elev.set_index('NAME')

for county in county_names:
    df.loc[county,'ELEV'] = round(elev.loc[county,'mean'],3)

df.to_csv(dir+'\\master.csv',index=True)

mtmp = pd.read_csv(dir+'\\Arkansas_Monthly_Mean_Temps_and_Precip_by_County.csv')
for i in range(len(mtmp)):
    mtmp.loc[i,'county_name'] = mtmp.loc[i,'county_name'].upper()
mtmp = mtmp.set_index('county_name')

for county in county_names:
    df.loc[county,'TMP2000'] = round(mtmp.loc[county,'mean temp (2000)'],3)
    df.loc[county,'TMP2010'] = round(mtmp.loc[county,'mean temp (2010)'],3)
    df.loc[county,'TMP2020'] = round(mtmp.loc[county,'mean temp (2020)'],3)
    df.loc[county,'PCP2000'] = round(mtmp.loc[county,'mean precip (2000)'],3)
    df.loc[county,'PCP2010'] = round(mtmp.loc[county,'mean precip (2010)'],3)
    df.loc[county,'PCP2020'] = round(mtmp.loc[county,'mean precip (2020)'],3)

df['DMGPOP2000'] = df['DMGCP2000'] / df['POP2000']  
df['DMGPOP2010'] = df['DMGCP2010'] / df['POP2000']  
df['DMGPOP2020'] = df['DMGCP2020'] / df['POP2020']  
    
df.to_csv(dir+'\\master.csv',index=True)




from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df)
scaled_df = pd.DataFrame(scaled_data, columns=df.columns, index=df.index)

# scaled_df.drop('FIPS',axis=1,inplace=True)
for county in county_names:
    scaled_df.loc[county,'FIPS'] = df.loc[county,'FIPS']

scaled_df.to_csv(dir+'\\master_scaled.csv',index=True)