import pandas as pd
import os

dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\Traffic Accidents\\Crashes.csv')

conditions = ['Ice or frost','Wet','Slush','Sleet','Snow',
              'Water (standing or moving)']

df = df[df['RoadwaySurfaceConidtion'].isin(conditions)]

event_counts = df[df['RoadwaySurfaceConidtion'].isin(conditions)]['RoadwaySurfaceConidtion'].value_counts()
# print(event_counts)

sum = event_counts.sum()
wntr_wx = (event_counts['Ice or frost'] + event_counts['Snow'] +\
      event_counts['Slush']) * 100 / sum
print(wntr_wx)