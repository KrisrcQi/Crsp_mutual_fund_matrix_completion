# -*- coding: utf-8 -*-
"""Return prediction of NAV by ANN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1wNW2y665tY_zgjZeBNKZ1iNjDGwn0eb7
"""

import numpy as np
import pandas as pd
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

!pip install jupyter_tensorboard

!pip install tensorflow tensorboard

# Step 1: read dataset and prepare data for ANN model training

df = pd.read_csv('Downsized 10k rows data with momentum.csv')
df

df_nav = df.iloc[:, 4]
df_nav

df_mtna = df.iloc[:, 3]
df_mtna

df_momentum = df.iloc[:, 5]
df_momentum

# Custom callback to display progress
class ProgressCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"Epoch {epoch + 1} - Time: {current_time} - MSE: {logs['loss']:.4f} - Accuracy: {logs['accuracy']:.4f}")

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
history = model.fit([X1_train, X2_train], y_train, epochs=40, batch_size=32, verbose=0, callbacks=[tensorboard_callback])

# Commented out IPython magic to ensure Python compatibility.
# Load the TensorBoard notebook extension
%load_ext tensorboard

%tensorboard --logdir=logs --port=6007

# Step 9: Make predictions on the test set
y_pred = model.predict([X1_test, X2_test])

y_test

y_pred

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