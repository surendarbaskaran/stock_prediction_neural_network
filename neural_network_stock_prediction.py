# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1rBzdcVHHVWDecT1TaK231QB5rKR0dEZJ
"""

import pandas as pd
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

df = pd.read_csv('nse_all_stock_data.csv',usecols=['TCS'])

df=df.dropna()
df=df.round(1)
df.head()

df.info()

X=np.array(df['TCS'])
X=X.reshape(-1,1)
X

plt.figure(figsize=(16,8))
plt.plot(df['TCS'])
plt.title('TCS')
plt.xlabel('Date',fontsize=18)
plt.ylabel('TCS')
plt.show()

temp=math.ceil(len(X)*0.8)
temp

#data scaling
scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(X)
scaled_data

#create training dataset
train_data=scaled_data[0:temp,:]
#split data to X_train and y_train
X_train=[]
y_train=[]
for i in range(60,len(train_data)):
    X_train.append(train_data[i-60:i,0])
    y_train.append(train_data[i,0])

#convert X_train and y_train to numpy array
X_train,y_train=np.array(X_train),np.array(y_train)
#Reshare the data
x_train=np.reshape(X_train,(X_train.shape[0],X_train.shape[1],1))
x_train.shape

#build LSTM model
model = Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(X_train.shape[1],1)))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(250))
model.add(Dense(1))

#compile the model
model.compile(optimizer='adam',loss='mean_squared_error')

#train the model
model.fit(x_train, y_train, batch_size=32, epochs=50)

#create a testing dataset
#create a new array containing scaled values from index 1543 to 2002z
test_data=scaled_data[temp-60:,:]
#create X_test and y_test
X_test=[]
y_test=X[temp:,:]
for i in range(60,len(test_data)):
    X_test.append(test_data[i-60:i,0])

#convert to a numpy array
X_test=np.array(X_test)

#reshape the data
x_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))

#get the models predicted price values
predictions=model.predict(x_test)
predictions=scaler.inverse_transform(predictions)

#get the root means square error
rmse=np.sqrt(np.mean(predictions-y_test)**2)
rmse

#plot predictions
train=df[:temp]
valid=df[temp:]
valid['Predictions']=predictions

plt.figure(figsize=(16,8))
plt.title('predicted')
plt.plot(train['TCS'])
plt.plot(valid[['TCS','Predictions']])
plt.xlabel('Date',fontsize=18)
plt.ylabel('TCS')
plt.legend(['Train','Val','Predictions'],loc='lower right')
plt.show()

valid

