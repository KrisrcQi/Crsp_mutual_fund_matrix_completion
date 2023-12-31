# -*- coding: utf-8 -*-
"""ANN model to predict fund return.ipynb


Original file is located at
    https://colab.research.google.com/drive/1wNW2y665tY_zgjZeBNKZ1iNjDGwn0eb7
"""
!pip install jupyter_tensorboard

!pip install tensorflow tensorboard


import numpy as np
import pandas as pd
import math
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, concatenate
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.callbacks import TensorBoard
from datetime import datetime



# Step 1: read dataset and prepare data for ANN model training

df = pd.read_csv('Downsized 10k rows data with momentum.csv')
df

# Checking the NAN in the data list of 'mtna'
nan_indices = []
for i, value in enumerate(df['mtna']):
    if math.isnan(value):
        nan_indices.append(i)

if nan_indices:
    print("The list contains NaN values at the following indices:")
    print(nan_indices)
else:
    print("The list does not contain NaN values.")

# filling 0 into NAN in the data list
for i, value in enumerate(df['mtna']):
    if math.isnan(value):
        df['mtna'][i] = 0

print("Updated data list:")
print(df['mtna'])

# Checking the NAN in the data list of 'mtna' again
nan_indices = []
for i, value in enumerate(df['mtna']):
    if math.isnan(value):
        nan_indices.append(i)

if nan_indices:
    print("The list contains NaN values at the following indices:")
    print(nan_indices)
else:
    print("The list does not contain NaN values.")

# Checking the NAN in the data list of 'mnav'
nan_indices = []
for i, value in enumerate(df['mnav']):
    if math.isnan(value):
        nan_indices.append(i)

if nan_indices:
    print("The list contains NaN values at the following indices:")
    print(nan_indices)
else:
    print("The list does not contain NaN values.")

# filling 0 into NAN in the data list
for i, value in enumerate(df['mnav']):
    if math.isnan(value):
        df['mnav'][i] = 0

print("Updated data list:")
print(df['mnav'])

# Checking the NAN in the data list of 'mnav' again
nan_indices = []
for i, value in enumerate(df['mnav']):
    if math.isnan(value):
        nan_indices.append(i)

if nan_indices:
    print("The list contains NaN values at the following indices:")
    print(nan_indices)
else:
    print("The list does not contain NaN values.")

# Checking the NAN in the data list of 'momentum'
nan_indices = []
for i, value in enumerate(df['momentum']):
    if math.isnan(value):
        nan_indices.append(i)

if nan_indices:
    print("The list contains NaN values at the following indices:")
    print(nan_indices)
else:
    print("The list does not contain NaN values.")

df_nav = df.iloc[:, 4]
df_nav

df_mtna = df.iloc[:, 3]
df_mtna

df_momentum = df.iloc[:, 5]
df_momentum

# Custom callback to display progress
class ProgressCallback(Callback):
    def on_train_begin(self, logs=None):
        self.start_time = datetime.now()

    def on_epoch_end(self, epoch, logs=None):
        elapsed_time = datetime.now() - self.start_time
        print(f"Epoch {epoch + 1} - Elapsed Time: {elapsed_time} - MSE: {logs['loss']:.4f}")
progress_callback = ProgressCallback()

# Step 2: Prepare the input and target data

X1 = df_momentum.values  # Input features from DataFrame 1
X2 = df_mtna.values  # Input features from DataFrame 2
y = df_nav.values  # Target variable

# Ensure the number of samples is consistent
num_samples = min(X1.shape[0], X2.shape[0], y.shape[0])
X1, X2, y = X1[:num_samples], X2[:num_samples], y[:num_samples]

# Step 3: Split the data into training and testing sets

X1_train, X1_test, X2_train, X2_test, y_train, y_test = train_test_split(X1, X2, y, test_size=0.2, random_state=42)

print("Shape of X1_train:", X1_train.shape)
print("Shape of X2_train:", X2_train.shape)
print("Shape of y_train:", y_train.shape)

# Reshape X1_train and X2_train to have a single column
X1_train = np.expand_dims(X1_train, axis=1)
X2_train = np.expand_dims(X2_train, axis=1)
y_train = np.expand_dims(y_train, axis=1)

print("Shape of X1_train:", X1_train.shape)
print("Shape of X2_train:", X2_train.shape)
print("Shape of y_train:", y_train.shape)

# Step 5: Define each layers

# input layers
input1 = Input(shape=(X1_train.shape[1],))
input2 = Input(shape=(X2_train.shape[1],))

# Concatenate the input layers
concatenated = concatenate([input1, input2])

# Add hidden layers
hidden1 = Dense(64, activation='relu')(concatenated)
hidden2 = Dense(64, activation='relu')(hidden1)

# Output layer
output = Dense(1)(hidden2)

# Step 6: Create the model
model = Model(inputs=[input1, input2], outputs=output)

# Step 7: Compile the model
model.compile(loss='mean_squared_error', optimizer='adam')

# Create the TensorBoard callback
tensorboard_callback = TensorBoard(log_dir='logs', histogram_freq=1)

# Step 8: Train the model and visualization training process
history = model.fit([X1_train, X2_train], y_train, epochs=200, batch_size=32, verbose=0, callbacks=[tensorboard_callback, progress_callback])

# Commented out IPython magic to ensure Python compatibility.
# Load the TensorBoard notebook extension
# %load_ext tensorboard

tensorboard --logdir=logs --port=6007

# Step 9: Make predictions on the test set

y_pred = model.predict([X1_test, X2_test])

y_pred_all = model.predict([X1, X2])

print(len(y_pred_all))

y_test

y_pred_all

# Assuming y_test and y_pred are NumPy arrays
# Assuming y_test and y_pred are not 1-dimensional arrays

y_test_1d = np.reshape(y_test, (-1,))
y_pred_1d = np.reshape(y_pred, (-1,))

nan_mask = np.isnan(y_test_1d) | np.isnan(y_pred_1d)
y_test_cleaned = y_test_1d[~nan_mask]
y_pred_cleaned = y_pred_1d[~nan_mask]

if len(y_test_cleaned) > 0:
    mse = mean_squared_error(y_test_cleaned, y_pred_cleaned)
    print('Mean Squared Error (MSE):', mse)
else:
    print('Error: No valid samples for evaluation.')

# Calculate accuracy rate (optional - depends on the nature of the problem)
accuracy = accuracy_score(np.round(y_test), np.round(y_pred))

print('Mean Squared Error (MSE):', mse)
print('Accuracy Rate:', accuracy)

# accumalted return

accumulated_returns = [0]
accumulated_return = 1  # Initial accumulated return is 1
individual_returns = []  # To store individual returns
for i in range(1, len(y_pred_all)):
    current_price = y_pred_all[i]
    previous_price = y_pred_all[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns.append(return_ratio)  # Append individual return
    accumulated_return *= (1 + return_ratio)
    accumulated_returns.append(accumulated_return)

# Printing individual returns
print("Individual Returns:")
for i, return_ratio in enumerate(individual_returns):
    print(f"Return at time {i + 1}: {accumulated_return + return_ratio}")

print("Accumulated return:")
print(accumulated_return)

print((len(individual_returns)))

individual_returns.insert(0, 0)
print(individual_returns)

print((len(individual_returns)))

import matplotlib.pyplot as plt


plt.figure(figsize=(300, 50))  # Specify the width and height in inches


# Plotting the accumulated returns
plt.plot(df['caldt'], individual_returns)
plt.xlabel('Time')
plt.ylabel('Accumulated Returns')
plt.title('Accumulated Returns over Time')
plt.show()


# plot first 12 funds return prediction in one graph


# Step 1, extracting the fist 12 funds data
fund_1 = y_pred_all[0:11]
fund_2 = y_pred_all[11:22]
fund_3 = y_pred_all[22:33]
fund_4 = y_pred_all[33:58]
fund_5 = y_pred_all[58:83]
fund_6 = y_pred_all[83:108]
fund_7 = y_pred_all[108:133]
fund_8 = y_pred_all[133:144]
fund_9 = y_pred_all[144:155]
fund_10 = y_pred_all[155:166]
fund_11 = y_pred_all[166:177]
fund_12 = y_pred_all[177:188]


# Step 2: Calculate each accumulated return for 12 funds
# accumalted return for fund 1
accumulated_returns_1 = [0]
accumulated_return_1 = 1  # Initial accumulated return is 1
individual_returns_1 = []  # To store individual returns
for i in range(1, len(fund_1)):
    current_price = fund_1[i]
    previous_price = fund_1[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_1.append(return_ratio)  # Append individual return
    accumulated_return_1 *= (1 + return_ratio)
    accumulated_returns_1.append(accumulated_return_1)

# Printing individual returns_1
print("Individual Returns_1:")
for i, return_ratio in enumerate(individual_returns_1):
    print(f"Return at time {i + 1}: {accumulated_return_1 + return_ratio}")

print("Accumulated return_1:")
print(accumulated_return_1)

# accumalted return for fund 2

accumulated_returns_2 = [0]
accumulated_return_2 = 1  # Initial accumulated return is 1
individual_returns_2 = []  # To store individual returns
for i in range(1, len(fund_2)):
    current_price = fund_2[i]
    previous_price = fund_2[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_2.append(return_ratio)  # Append individual return
    accumulated_return_2 *= (1 + return_ratio)
    accumulated_returns_2.append(accumulated_return_2)

# Printing individual returns_2
print("Individual Returns_2:")
for i, return_ratio in enumerate(individual_returns_2):
    print(f"Return at time {i + 1}: {accumulated_return_2 + return_ratio}")

print("Accumulated return_2:")
print(accumulated_return_2)

# accumalted return for fund 3

accumulated_returns_3 = [0]
accumulated_return_3 = 1  # Initial accumulated return is 1
individual_returns_3 = []  # To store individual returns
for i in range(1, len(fund_3)):
    current_price = fund_3[i]
    previous_price = fund_3[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_3.append(return_ratio)  # Append individual return
    accumulated_return_3 *= (1 + return_ratio)
    accumulated_returns_3.append(accumulated_return_3)

# Printing individual returns_3
print("Individual Returns_3:")
for i, return_ratio in enumerate(individual_returns_3):
    print(f"Return at time {i + 1}: {accumulated_return_3 + return_ratio}")

print("Accumulated return_3:")
print(accumulated_return_3)

# accumalted return for fund 4

accumulated_returns_4 = [0]
accumulated_return_4 = 1  # Initial accumulated return is 1
individual_returns_4 = []  # To store individual returns
for i in range(1, len(fund_4)):
    current_price = fund_4[i]
    previous_price = fund_4[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_4.append(return_ratio)  # Append individual return
    accumulated_return_4 *= (1 + return_ratio)
    accumulated_returns_4.append(accumulated_return_4)

# Printing individual returns_4
print("Individual Returns_4:")
for i, return_ratio in enumerate(individual_returns_4):
    print(f"Return at time {i + 1}: {accumulated_return_4 + return_ratio}")

print("Accumulated return_4:")
print(accumulated_return_4)

# accumalted return for fund 5

accumulated_returns_5 = [0]
accumulated_return_5 = 1  # Initial accumulated return is 1
individual_returns_5 = []  # To store individual returns
for i in range(1, len(fund_5)):
    current_price = fund_5[i]
    previous_price = fund_5[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_5.append(return_ratio)  # Append individual return
    accumulated_return_5 *= (1 + return_ratio)
    accumulated_returns_5.append(accumulated_return_5)

# Printing individual returns_5
print("Individual Returns_5:")
for i, return_ratio in enumerate(individual_returns_5):
    print(f"Return at time {i + 1}: {accumulated_return_5 + return_ratio}")

print("Accumulated return_5:")
print(accumulated_return_5)

# accumalted return for fund 6

accumulated_returns_6 = [0]
accumulated_return_6 = 1  # Initial accumulated return is 1
individual_returns_6 = []  # To store individual returns
for i in range(1, len(fund_6)):
    current_price = fund_6[i]
    previous_price = fund_6[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_6.append(return_ratio)  # Append individual return
    accumulated_return_6 *= (1 + return_ratio)
    accumulated_returns_6.append(accumulated_return_6)

# Printing individual returns_6
print("Individual Returns_6:")
for i, return_ratio in enumerate(individual_returns_6):
    print(f"Return at time {i + 1}: {accumulated_return_6 + return_ratio}")

print("Accumulated return_6:")
print(accumulated_return_6)

# accumalted return for fund 7

accumulated_returns_7 = [0]
accumulated_return_7 = 1  # Initial accumulated return is 1
individual_returns_7 = []  # To store individual returns
for i in range(1, len(fund_7)):
    current_price = fund_7[i]
    previous_price = fund_7[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_7.append(return_ratio)  # Append individual return
    accumulated_return_7 *= (1 + return_ratio)
    accumulated_returns_7.append(accumulated_return_7)

# Printing individual returns_7
print("Individual Returns_7:")
for i, return_ratio in enumerate(individual_returns_7):
    print(f"Return at time {i + 1}: {accumulated_return_7 + return_ratio}")

print("Accumulated return_7:")
print(accumulated_return_7)

# accumalted return for fund 8

accumulated_returns_8 = [0]
accumulated_return_8 = 1  # Initial accumulated return is 1
individual_returns_8 = []  # To store individual returns
for i in range(1, len(fund_8)):
    current_price = fund_8[i]
    previous_price = fund_8[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_8.append(return_ratio)  # Append individual return
    accumulated_return_8 *= (1 + return_ratio)
    accumulated_returns_8.append(accumulated_return_8)

# Printing individual returns_8
print("Individual Returns_8:")
for i, return_ratio in enumerate(individual_returns_8):
    print(f"Return at time {i + 1}: {accumulated_return_8 + return_ratio}")

print("Accumulated return_8:")
print(accumulated_return_8)

# accumalted return for fund 9

accumulated_returns_9 = [0]
accumulated_return_9 = 1  # Initial accumulated return is 1
individual_returns_9 = []  # To store individual returns
for i in range(1, len(fund_9)):
    current_price = fund_9[i]
    previous_price = fund_9[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_9.append(return_ratio)  # Append individual return
    accumulated_return_9 *= (1 + return_ratio)
    accumulated_returns_9.append(accumulated_return_9)

# Printing individual returns_9
print("Individual Returns_9:")
for i, return_ratio in enumerate(individual_returns_9):
    print(f"Return at time {i + 1}: {accumulated_return_9 + return_ratio}")

print("Accumulated return_9:")
print(accumulated_return_9)

# accumalted return for fund 10

accumulated_returns_10 = [0]
accumulated_return_10 = 1  # Initial accumulated return is 1
individual_returns_10 = []  # To store individual returns
for i in range(1, len(fund_10)):
    current_price = fund_10[i]
    previous_price = fund_10[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_10.append(return_ratio)  # Append individual return
    accumulated_return_10 *= (1 + return_ratio)
    accumulated_returns_10.append(accumulated_return_10)

# Printing individual returns_10
print("Individual Returns_10:")
for i, return_ratio in enumerate(individual_returns_10):
    print(f"Return at time {i + 1}: {accumulated_return_10 + return_ratio}")

print("Accumulated return_10:")
print(accumulated_return_10)

# accumalted return for fund 11

accumulated_returns_11 = [0]
accumulated_return_11 = 1  # Initial accumulated return is 1
individual_returns_11 = []  # To store individual returns
for i in range(1, len(fund_11)):
    current_price = fund_11[i]
    previous_price = fund_11[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_11.append(return_ratio)  # Append individual return
    accumulated_return_11 *= (1 + return_ratio)
    accumulated_returns_11.append(accumulated_return_11)

# Printing individual returns_11
print("Individual Returns_11:")
for i, return_ratio in enumerate(individual_returns_11):
    print(f"Return at time {i + 1}: {accumulated_return_11 + return_ratio}")

print("Accumulated return_11:")
print(accumulated_return_11)

# accumalted return for fund 12


accumulated_returns_12 = [0]
accumulated_return_12 = 1  # Initial accumulated return is 1
individual_returns_12 = []  # To store individual returns
for i in range(1, len(fund_12)):
    current_price = fund_12[i]
    previous_price = fund_12[i - 1]
    return_ratio = (current_price - previous_price) / previous_price
    individual_returns_12.append(return_ratio)  # Append individual return
    accumulated_return_12 *= (1 + return_ratio)
    accumulated_returns_12.append(accumulated_return_12)

# Printing individual returns_12
print("Individual Returns_12:")
for i, return_ratio in enumerate(individual_returns_12):
    print(f"Return at time {i + 1}: {accumulated_return_12 + return_ratio}")

print("Accumulated return_12:")
print(accumulated_return_12)

# Step 3: Plotting graph 
# Create a list of funds
funds = [individual_returns_1, individual_returns_2, individual_returns_3, individual_returns_4, individual_returns_5, individual_returns_6, individual_returns_7, individual_returns_8, individual_returns_9, individual_returns_10, individual_returns_11, individual_returns_12]

# Create a line style for each fund
line_styles = ['-', '--', ':', '-.', '-', '--', ':', '-.', '-', '--', ':', '-.']

# Plot each fund on the graph
for i, fund in enumerate(funds):
    plt.plot(fund, linestyle=line_styles[i])

# Set the labels and title of the graph
plt.xlabel('Fund hold months')
plt.ylabel('Accumulated return')
plt.title('Comparison of 12 Funds')

# Display the legend
plt.legend(['Fund {}'.format(i+1) for i in range(len(funds))])


plt.figure(figsize=(100, 50))  # Specify the width and height in inches

# Display the graph
plt.show()

plt.savefig('comparison_plot1.jpeg')
