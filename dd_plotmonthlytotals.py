import pandas as pd
import os 
import matplotlib.pyplot as plt

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

months = ['October','November','December','January','February','March','April','May']
event_types = ["Heavy Snow", "Winter Storm", "Winter Weather", "Ice Storm"]

colors = ['darkblue','blue','lightblue','purple']
for event in event_types:
    snow = df[df['EVENT_TYPE']==event]
    monthly_events = snow.groupby('MONTH_NAME')['EPISODE_ID'].nunique().sort_index()
    plt.figure(figsize=(10, 6))
    monthly_events.plot(kind='bar', color=colors[event_types.index(event)])
    plt.ylabel('Number of '+event+' events')
    plt.xlabel('')
    plt.title('Number of '+event+' events by month in AR (1996-2024)')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(dir+'\\Images\\Monthly bar plots for '+event+'.png')



monthly_events = df.groupby('MONTH_NAME')['EPISODE_ID'].nunique().sort_index()
plt.figure(figsize=(10, 6))
monthly_events.plot(kind='bar', color='skyblue')
plt.ylabel('Number of winter related events')
plt.xlabel('')
plt.title('Number of winter-related events by month in AR (1996-2024)')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(dir+'\\Images\\Monthly bar plots.png')