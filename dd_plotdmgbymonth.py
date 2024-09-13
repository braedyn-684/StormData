import pandas as pd
import os 
import matplotlib.pyplot as plt

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'])
df['MONTH'] = df['BEGIN_DATE_TIME'].dt.month

event_types = ['Winter Storm', 'Ice Storm', 'Winter Weather','Ice Storm']
funding_by_month = df.groupby(['MONTH','EVENT_TYPE'])['DAMAGE_PROPERTY_CPI'].sum().unstack(fill_value=0)

month_order = [10, 11, 12, 1, 2, 3, 4, 5]
months = ['October','November','December','January','February','March','April','May']

funding_by_month = funding_by_month.loc[month_order]

colors=['blue','purple','lightblue','darkblue']


fig, ax1 = plt.subplots(figsize = (10, 6))
funding_by_month.plot(kind='bar',stacked=True,color=colors,ax=plt.gca())
ax1.set_xticks(range(len(months)))
ax1.set_xticklabels(months)
plt.title('Damage by month/type in Arkansas with CPI adjustment')
plt.ylabel('Total Federal Funding ($)')
plt.xticks(rotation=0)
plt.xlabel('')
yticks = ax1.get_yticks()
# ax1.set_ylim(0,3100000000)
ax1.set_yticklabels([f'${y/1e6:.0f}M' for y in yticks])
plt.savefig(dir+'\\Damage by month_type bar plots.png')