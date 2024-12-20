import pandas as pd
import os
from datetime import datetime

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\master.csv')

summary_df = df.describe().loc[['min', 'max', 'mean', 'std']]
summary_df = summary_df.T

summary_df.to_csv(dir+'\\master_statistics.csv',index=True)