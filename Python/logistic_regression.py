import numpy as np 
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import pickle



pre_data = pd.read_csv('df-preprocessed.csv')

# Create the targets:
targets = np.where(pre_data['Absenteeism Time in Hours'] > 
                   pre_data['Absenteeism Time in Hours'].median(), 1, 0)
pre_data['Excessive_Absenteeism'] = targets
data_with_targets = pre_data.drop(['Absenteeism Time in Hours'], axis=1)
unscaled_inputs = data_with_targets.iloc[:, :-1]

# Create the customer scaler class:
class CustomScaler(BaseEstimator, TransformerMixin):
    
    def __init__(self, columns, copy=True, with_mean=True, with_std=True):
        self.scaler = StandardScaler(copy, with_mean, with_std)
        self.columns = columns
        self.mean_ = None
        self.var_ = None
        
    def fit(self, X, y=None):
        self.scaler.fit(X[self.columns], y)
        self.mean_ = np.mean(X[self.columns])
        self.var_ = np.var(X[self.columns])
        return self

    def transform(self, X, y=None, copy=None):
        init_col_order = X.columns
        X_scaled = pd.DataFrame(self.scaler.transform(X[self.columns]), 
                               columns = self.columns)
        X_not_scaled = X.loc[:, ~X.columns.isin(self.columns)]
        return pd.concat([X_not_scaled, X_scaled], axis=1)[init_col_order]       

# Scale the data:
columns_to_omit = ['Reason_1', 'Reason_2', 'Reason_3', 'Reason_4', 'Education']
columns_to_scale = [x for x in unscaled_inputs.columns.values if x not in columns_to_omit]
absentee_scaler = CustomScaler(columns_to_scale)


# Fit/transform the data:
absentee_scaler.fit(unscaled_inputs)
scaled_inputs = absentee_scaler.transform(unscaled_inputs)

# Train/Test the data:
x_train, x_test, y_train, y_test = train_test_split(scaled_inputs, targets, random_state = 20, train_size = 0.8)
         

# Logistic Regression Analysis: 
reg = LogisticRegression()
reg.fit(x_train, y_train)
model_outputs = reg.predict(x_train)


# Look at the results of the data with a 'summary table':
feature_name = unscaled_inputs.columns.values
summary_table = pd.DataFrame(columns=['Feature Name'],
                             data = feature_name)
summary_table['Coefficients'] = np.transpose(reg.coef_)
summary_table.index = summary_table.index + 1
summary_table.loc[0] = ['Intercept', reg.intercept_[0]]
summary_table = summary_table.sort_index()
summary_table['Odds_ratio'] = np.exp(summary_table.Coefficients)
summary_table.sort_values('Odds_ratio', ascending=False, inplace=True)
print(summary_table.to_string())

# Predicted Probability:
predicted_probability = reg.predict_proba(x_test)


# Export the pickle:
# model_file => newly created filename
# wb => write bytes; or rb => read bytes for unpickeling
# dump => save info to file ; or load => load info from file for unpickeling
# reg => object to tbe dump

with open('model.pkl', 'wb') as file:
    pickle.dump(reg, file)

with open('model.pkl', 'rb') as file:
    mp = pickle.load(file)

reg.predict(x_train)
with open('scaler_file.pkl', 'wb') as file:
    pickle.dump(absentee_scaler, file)
         
         
         
         
