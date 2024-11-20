import pandas as pd
import os
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df0 = pd.read_csv(dir+'\\Storm Data CPI.csv')

CWAs = ['Tulsa','Little Rock','Shreveport','Memphis','Jackson']

tulsa = ['Madison', 'Crawford', 'Sebastian', 'Carroll', 
          'Washington', 'Benton', 'Franklin']
TULSA = [x.upper() for x in tulsa]
little_rock = ['Johnson', 'Pope', 'Stone', 'Searcy', 'Izard',
               'Newton', 'Independence', 'Franklin', 'Van Buren', 
               'Yell', 'Polk', 'Cleburne', 'Logan', 'Scott', 
               'Boone', 'Fulton', 'Sharp', 'Marion', 'Baxter', 
               'Clark', 'Pulaski', 'Lonoke', 'Conway', 'Faulkner', 
               'White', 'Hot Spring', 'Grant', 'Montgomery', 
               'Garland', 'Saline', 'Jackson', 'Pike', 'Prairie', 
               'Monroe', 'Jefferson', 'Dallas', 'Cleveland', 
               'Arkansas', 'Perry', 'Woodruff', 'Lincoln', 
               'Ouachita', 'Drew', 'Bradley', 'Calhoun', 'Desha', 
               'Randolph', 'Lawrence']
LITTLE_ROCK = [x.upper() for x in little_rock]
shreveport = ['Miller', 'Nevada', 'Union', 'Columbia', 
              'Little River', 'Hempstead', 'Sevier', 
              'Howard', 'Lafayette']
SHREVEPORT = [x.upper() for x in shreveport]
memphis = ['Randolph', 'Clay', 'Lawrence', 'Greene', 'Phillips', 
           'Craighead', 'St. Francis', 'Lee', 'Mississippi', 
           'Crittenden', 'Cross', 'Poinsett']
MEMPHIS = [x.upper() for x in memphis]
jackson = ['Ashley','Chicot']
JACKSON = [x.upper() for x in jackson]


def count_frequency(counties):
    filtered = df0[df0['CZ_NAME'].isin(counties)]
    count_freq = len(filtered)/len(counties)
    return count_freq

def dmg_frequency(counties):
    filtered = df0[df0['CZ_NAME'].isin(counties)]
    filtered_dmg = filtered[(filtered['DAMAGE_PROPERTY_CPI']>0) &\
                             (filtered['DAMAGE_PROPERTY_CPI']<4000000000)]
    dmg_frq = len(filtered_dmg)*100/len(filtered)
    return dmg_frq

print('CWA\t\tcount/county\tdmg freq')
print('----------------------------------------')
tsa = count_frequency(TULSA)
tsa_dmg = dmg_frequency(TULSA)
print(CWAs[0]+'\t\t'+str(round(tsa,2))+''+'\t\t'+str(round(tsa_dmg,2))+'%')
lzk = count_frequency(LITTLE_ROCK)
lzk_dmg = dmg_frequency(LITTLE_ROCK)
print(CWAs[1]+'\t'+str(round(lzk,2))+''+'\t\t'+str(round(lzk_dmg,2))+'%')
shv = count_frequency(SHREVEPORT)
shv_dmg = dmg_frequency(SHREVEPORT)
print(CWAs[2]+'\t'+str(round(shv,2))+''+'\t\t'+str(round(shv_dmg,2))+'%')
meg = count_frequency(MEMPHIS)
meg_dmg = dmg_frequency(MEMPHIS)
print(CWAs[3]+'\t\t'+str(round(meg,2))+''+'\t\t'+str(round(meg_dmg,2))+'%')
jan = count_frequency(JACKSON)
jan_dmg = dmg_frequency(JACKSON)
print(CWAs[4]+'\t\t'+str(round(jan,2))+''+'\t\t'+str(round(jan_dmg,2))+'%')