import pandas as pd


raw_csv_data = pd.read_csv('Absenteeism-data.csv')

# Initial set up
df_copy = raw_csv_data.copy()
df_copy.drop('ID', axis = 1, inplace = True)
reasons_column = pd.get_dummies(df_copy['Reason for Absence'])
df_copy = df_copy.drop('Reason for Absence', axis = 1)
df_copy = pd.concat([df_copy, reason_type_1, reason_type_2, 
                     reason_type_3, reason_type_4], axis = 1)


# Column title restructuring:
df_copy.rename(columns = {0: 'Reason_Type_1', 1: 'Reason_Type_2', 
                          2 : 'Reason_Type_3', 3 : 'Reason_Type_4'},
               inplace=True)
columns_reordered = ['Reason_Type_1','Reason_Type_2','Reason_Type_3','Reason_Type_4','Date', 'Transportation Expense', 'Distance to Work', 'Age',
       'Daily Work Load Average', 'Body Mass Index', 'Education',
       'Children', 'Pets', 'Absenteeism Time in Hours']
df_copy = df_copy[columns_reordered]
df_reason_mod = df_copy.copy()



# Working with the dates:
df_reason_mod['Date'] = pd.to_datetime(df_reason_mod['Date'],
                                      format = '%d/%m/%Y')
list_months = []
for i in range(df_reason_mod.shape[0]):
    list_months.append(df_reason_mod['Date'][i].month)
df_reason_mod['Month Value'] = list_months

def weekday_maker(date_value):
    return date_value.weekday()
weekday_obj = df_reason_mod['Date'].apply(weekday_maker)
df_reason_mod['Day of the Week'] = weekday_obj


# Mapping educaiton levels:
df_reason_mod['Education'] = df_reason_mod['Education'].map({1:0, 2:1, 3:1, 4:1})


# Export the preprocessed csv:
df_preprocessed = df_reason_mod.copy()
new_csv_data = df_preprocessed.to_csv(index=False, encoding='utf-8')
    
