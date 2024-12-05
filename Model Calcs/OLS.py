import pandas as pd
import numpy as np
import os
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
dir = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(dir+'\\master_scaled.csv')

Y = df['DMGPOP2000']
X = df[['HS2020','WS2020','IS2020','HOURS20','MGRCP2020',
        'PNW2020','MICPI2020','AG21','FOR21','URB21','WAT21','ELEV','TMP2020','PCP2020','SNW2020']]
X = df[['HS2000','WS2000','IS2000','HOURS00','ELEV','SNW2000']]
# X = df[['WS2010','HOURS10','MICPI2010','FOR11','WAT11','ELEV','PCP2010']]
# X = df[['IS2020','AG21','FOR21','ELEV','TMP2020']]

# X = df[['FOR01','TMP2000']]
# X = df[['PNW2000','AG01','FOR01','TMP2000','PCP2000','SNW2000']]
# X = df[['FOR11','URB11','ELEV','PCP2010']]
# X = df[['AG21','FOR21','ELEV','SNW2020']]

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
# styled_table = correlation_matrix.style.background_gradient(cmap='coolwarm').format(precision=2)
# styled_table.to_html(dir+'\\Images\\Round_6_2000_Cor_matrix.html')