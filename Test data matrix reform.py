import pandas as pd
import numpy as np
from datetime import datetime

# Reading the data file
# Checking the empty cells in the dataset
df = pd.read_stata('/Users/ruochenqi/Documents/Fintech in UofG/Dissertation/Data/02f5113657d72eaa.dta')
print(df)
small_date = df['caldt'].min()
print(small_date)
max_date = df['caldt'].max()
print(max_date)

# Downsizing the original dataframe for testing the program
df = df[:633]

# Drop other two input data
df_1 = df.drop(['mtna','mret'], axis=1)
print(df_1)
small_date_1 = df_1['caldt'].min()
print(small_date_1)
max_date_1 = df_1['caldt'].max()
print(max_date_1)

print("{:=^150s}".format("Split Line"))



first_column = df_1.iloc[:, 0]
# unique_second_column = np.unique(df1.iloc[:, 1])
second_column = df_1.iloc[:, 1]
third_column = df_1.iloc[:, 2]


# convert the data "caldt" from timestampe to string
print(type(first_column[0]))
print(type(first_column))
print(first_column)

str_first_column = []
for timestamp_str in first_column:
    timestamp_str = timestamp_str.strftime('%Y-%m')
    str_first_column.append(timestamp_str)


df_1['caldt'] = str_first_column
print(df_1)
print(type(df_1.iloc[0]['caldt']))
print("{:=^150s}".format("Split Line"))

print(type(second_column))
print(second_column)

for int_fundno in second_column:
    int_fundno = int(int_fundno)
print(type(int_fundno))


# df['crsp_fundno'] = second_column
print("{:=^150s}".format("Split Line"))


mf_id = list(range(1, 11))
# Create an empty DataFrame
# Create a date range from '1961-12' to '2020-04'
date_range = pd.date_range('1983-12', '2000-08', freq='M')

# Create a new DataFrame with the 'date' column
df_2 = pd.DataFrame({'date': date_range})

# Convert the 'date' column to string datatype
df_2['date'] = df_2['date'].dt.strftime('%Y-%m')

column_names = [i for i in range(1, 11)]
df_2 = pd.concat([df_2, pd.DataFrame(columns=column_names)], ignore_index=True)

print(df_2)

for i in range(len(mf_id)):
  for j in range(len(df_1)):
    for k in range(len(df_2)):
      if (df_1.iloc[j]['crsp_fundno']) == mf_id[i]:
        if(df_1.iloc[j]['caldt']) == df_2.iloc[k]['date']:
          df_2.iloc[k, i+1] = df_1.iloc[j]['mnav']

print(df_2)
df_2.to_csv('/Users/ruochenqi/Documents/Fintech in UofG/Dissertation/Data/Matrix_NAV.csv')


