import pandas as pd
import os 
import matplotlib.pyplot as plt
import numpy as np


dir = os.path.dirname(os.path.abspath(__file__))
# df = pd.read_csv(dir+'\\Boxplot\\GWR2000.csv')

# x = df['y']
# y = df['x']
# y_labels = ['#HS','#WS','%R','Hrs','Snw']
# y_pos = [1, 2, 3, 4, 5]


# plt.scatter(x,y)
# # plt.ylim(1,5,1)
# plt.yticks(y_pos, y_labels)
# plt.xlabel('Coefficient')
# plt.title('Coefficients of the 2000 GWR Model')
# plt.gca().invert_yaxis()
# plt.grid()
# plt.xticks(np.arange(-2.5,6.6,1))
# plt.plot()
# plt.close()


df = pd.read_csv(dir+'\\Boxplot\\MGWR2010.csv')

x = df['y']
y = df['x']
y_labels = ['%R','Hrs','Inc','%DF','%Wat','Elv','Pcp','Snw']
y_pos = [1, 2, 3, 4, 5, 6, 7, 8]


plt.scatter(x,y)
# plt.ylim(1,5,1)
plt.yticks(y_pos, y_labels)
plt.xlabel('Coefficient')
plt.title('Coefficients of the 2010 MGWR Model')
plt.gca().invert_yaxis()
plt.grid()
# plt.xticks(np.arange(-2.5,6.6,1))
plt.plot()
