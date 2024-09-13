import pandas as pd
import os 
import matplotlib.pyplot as plt

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Storm Data CPI.csv')

funding_by_type = df.groupby('EVENT_TYPE')['DAMAGE_PROPERTY_CPI'].sum()
funding_filtered = funding_by_type[['Winter Storm', 'Ice Storm', 'Winter Weather','Ice Storm']]

ax = funding_by_type.plot(kind='bar', color=['blue','purple','lightblue','darkblue'])

plt.title('Damage by type in Arkansas with CPI adjustment')
plt.ylabel('Total Federal Funding ($)')
plt.xticks(rotation=0)
plt.xlabel('')
yticks = ax.get_yticks()
ax.set_yticklabels([f'${y/1e6:.0f}M' for y in yticks])
plt.savefig(dir+'\\Damage by type bar plots.png')