import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\master_scaled.csv')

Y = df['DMGPOP2010']
# X = df[['MGRCP2000','PNW2000','MICPI2000','AG01','FOR01','URB01','WAT01','ELEV','TMP2000','PCP2000','SNW2000']]
# X = df[['PCP2000']]
# X = df[['FOR01','TMP2000']]
X = df[['AG11','FOR11','URB11','ELEV','PCP2010']]
# X = df[['MGRCP2010','FOR11','ELEV','PCP2010']]
# X = df[['AG21','FOR21','ELEV','TMP2020']]

X = sm.add_constant(X)
model = sm.OLS(Y,X).fit()
print(model.summary())

vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i)
                          for i in range(len(X.columns))]

print(' ')
print(vif_data)


# import seaborn as sns
# import matplotlib.pyplot as plt

# correlation_matrix = X.corr()
# print(correlation_matrix)
# plt.figure(figsize=(10, 8))
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", 
#             annot_kws={"size": 10}, square=True, cbar_kws={'shrink': .8})
# plt.title('Correlation Matrix')
# plt.show()
# correlation_matrix.style.background_gradient(cmap='coolwarm').format(precision=2)