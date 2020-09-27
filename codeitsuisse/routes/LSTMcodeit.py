#importing required libraries
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import pandas as pd
import numpy as np
import logging
import json
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/pre-tick', methods=['POST'])
def evaluate():
    data = request.get_json()
    df = pd.read_csv(data)
    new_data = df[['Close']]
    result = LSTM(new_data)
    return json.dumps(result)


#creating train and test sets
def LSTM(new_data):
    dataset = new_data.values

    train = dataset[0:2000, :]
    valid = dataset[987:, :]

    #converting dataset into x_train and y_train
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)

    x_train, y_train = [], []
    for i in range(100, len(train)):
        x_train.append(scaled_data[i - 100:i, 0])
        y_train.append(scaled_data[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True,
              input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dense(1))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(x_train, y_train, epochs=1, batch_size=1, verbose=2)

    #predicting 246 values, using past 60 from the train data
    inputs = new_data[1900:].values
    inputs = inputs.reshape(-1, 1)
    inputs = scaler.transform(inputs)

    X_test = [inputs]
    #for i in range(60, inputs.shape[0]):
        #X_test.append(inputs[i - 60:i, 0])
    X_test = np.array(X_test)

    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    closing_price = model.predict(X_test)
    closing_price = scaler.inverse_transform(closing_price)
    return closing_price[0][0]

