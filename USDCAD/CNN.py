import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import yfinance as yf

from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from keras.layers import Conv1D, MaxPooling1D, Flatten

currency = 'USDCAD=X'

start = dt.datetime(2021, 1, 1)
end = dt.datetime(2023, 10, 1)

data = yf.Ticker(currency).history(start=start, end=end)

# prepare data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1, 1))

prediction_days = 60

x_train = []
y_train = []

for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x - prediction_days: x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Build the CNN model
model = Sequential()

model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(x_train.shape[1], 1)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dense(50, activation='relu'))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32)

# Load Test Data
test_start = dt.datetime(2023, 7, 1)
test_end = dt.datetime.now()

test_data = yf.Ticker(currency).history(start=test_start, end=test_end)
actual_prices = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

# Make Predictions on Test Data

x_test = []

for x in range(prediction_days, len(model_inputs)):
    x_test.append(model_inputs[x - prediction_days:x, 0])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

# Plot the Test Predictions
plt.plot(actual_prices, color="black", label=f"Actual {currency} Price")
plt.plot(predicted_prices, color="green", label=f"Predicted {currency} Price")
plt.title(f"{currency} Shared Price")
plt.xlabel('Time')
plt.ylabel(f'{currency} Shared Price')
plt.legend()
plt.show()

# predict Next Day

# real_data = [model_inputs[len(model_inputs) + 1 - prediction_days: len(model_inputs) + 1, 0]]
# real_data = np.array(real_data)
# real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
#
# prediction = model.predict(real_data)
# predict Next Day
real_data = [model_inputs[-prediction_days:, 0]]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1], 1))
prediction = model.predict(real_data)

prediction = scaler.inverse_transform(prediction)
print(f"Predictoin: {prediction}")

# Calculate performance metrics
mae = mean_absolute_error(actual_prices, predicted_prices)
rmse = mean_squared_error(actual_prices, predicted_prices, squared=False)
r2 = r2_score(actual_prices, predicted_prices)

print(f"Mean Absolute Error (MAE): ${mae:.2f}")
print(f"Root Mean Square Error (RMSE): ${rmse:.2f}")
print(f"R2 Score: {r2:.2f}")
