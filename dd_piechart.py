import pandas as pd
import os 
import matplotlib.pyplot as plt


dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

event_types = ["Heavy Snow", "Winter Storm", "Winter Weather", "Ice Storm"]
color=['darkblue','blue','lightblue','purple']


event_counts = df[df['EVENT_TYPE'].isin(event_types)]['EVENT_TYPE'].value_counts()
counts = [event_counts.get(event, 0) for event in event_types]


funding_by_type = df.groupby('EVENT_TYPE')['DAMAGE_PROPERTY_CPI'].sum()
funding_filtered = funding_by_type[["Heavy Snow", "Winter Storm", "Winter Weather", "Ice Storm"]]

costs = funding_filtered.tolist()

plt.pie(counts,colors=color) #,labels=event_types,colors=color, autopct='%1.1f%%')
# plt.title('Number of reports')
plt.savefig(dir+'\\Images\\Pie chart counts.png')
# plt.show()


plt.pie(costs,colors=color, )#, labels=event_types,colors=color, autopct='%1.1f%%')
# plt.title('Property damage ($ - CPI Adjusted)')
plt.savefig(dir+'\\Images\\Pie chart damages.png')