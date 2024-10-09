import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, '')
import os
dir = os.path.dirname(os.path.abspath(__file__))

HS = pd.read_csv(dir+'\\State Rankings Heavy Snow.csv')
States = HS['STATE']
HS.set_index('STATE', inplace=True)
IS = pd.read_csv(dir+'\\State Rankings Ice Storm.csv')
IS.set_index('STATE', inplace=True)
WS = pd.read_csv(dir+'\\State Rankings Winter Storm.csv')
WS.set_index('STATE', inplace=True)
WW = pd.read_csv(dir+'\\State Rankings Winter Weather.csv')
WW.set_index('STATE', inplace=True)
ALL = pd.read_csv(dir+'\\State Rankings.csv')
ALL.set_index('STATE', inplace=True)



df = pd.DataFrame(index=States)
events = ['HS','IS','WS','WW','ALL']
event_dfs = [HS,IS,WS,WW,ALL]
event_names = ['Heavy Snow','Ice Storm','Winter Storm','Winter Weather','All']
var = ['DD','ID','DI','II','CPI']
var_full = ['DEATHS_DIRECT','DEATHS_INDIRECT','INJURIES_DIRECT',
            'INJURIES_INDIRECT','DAMAGE_PROPERTY_CPI']
var_names = ['Direct Deaths','Indirect Deaths','Direct Injuries',
             'Indirect Injuries','CPI-Adj. Damage']

for e in range(5):
    for v in range(5): 
        df[events[e]+' '+var[v]] = event_dfs[e][var_full[v]]

for e in range(5):
    for v in range(5): 
        df[events[e]+' '+var[v]+' Rank'] = df[events[e]+' '+var[v]].rank(ascending=False,method='max')

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

# for e in range(5):
#     print('Arkansas\'s rank for '+event_names[e]+' events:')
#     for v in range(5):
#         rank = round(df.loc['ARKANSAS', events[e] + ' ' + var[v] + ' Rank'])
#         if v == 4:
#             print(var_names[v]+': '+ordinal(rank)+\
#               ' ('+str(locale.currency(df.loc['ARKANSAS',events[e]+' '+var[v]],grouping=True))+')')
#         else:
#             print(var_names[v]+': '+ordinal(rank)+\
#               ' ('+str(df.loc['ARKANSAS',events[e]+' '+var[v]])+')')


summary_data = []
for e in range(5):
    for v in range(5): 
        rank = round(df.loc['ARKANSAS', events[e] + ' ' + var[v] + ' Rank'])
        if v == 4:
            value = locale.currency(df.loc['ARKANSAS',events[e]+' '+var[v]],grouping=True)
        else:
            value = str(df.loc['ARKANSAS',events[e]+' '+var[v]])
        
        summary_data.append({
            'Event': event_names[e],
            'Variable': var_names[v],
            'Rank': ordinal(rank),
            'Value':value
        })

summary_df = pd.DataFrame(summary_data)
print(summary_df)
summary_df.to_csv(dir+'\\Arkansas Rankings.csv', index=False)


rank_one_data = []
for e in range(5):
    for v in range(5): 
        top_state = df[df[events[e]+' '+var[v]+' Rank'] == 1.0].index#.tolist()
        rank = 1
        if v == 4:
            value = locale.currency(df.loc[top_state[0],events[e]+' '+var[v]],grouping=True)
        else:
            value = str(df.loc[top_state[0],events[e]+' '+var[v]])
        rank_one_data.append({
            'Event': event_names[e],
            'Variable': var_names[v],
            'State': top_state[0],
            'Rank': ordinal(rank),
            'Value':value
        })

rank_one_df = pd.DataFrame(rank_one_data)
print(rank_one_df)
rank_one_df.to_csv(dir+'\\Rank One Rankings.csv', index=False)