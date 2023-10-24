import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Fetching the data
currency = 'AAL'
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2023, 7, 1)
data = yf.Ticker(currency).history(start=start, end=end)
prices = data['Close'].values

# Split data into train and test sets
train_size = int(len(prices) * 0.8)
train, test = prices[:train_size], prices[train_size:]

# ARIMA model
# As previously mentioned, you may need to adjust the (p,d,q) parameters based on your data's characteristics.
model = ARIMA(train, order=(5,1,0))
model_fit = model.fit()

# Forecast
forecast = model_fit.forecast(steps=len(test))


# Plot actual vs predicted values
plt.figure(figsize=(15, 7))
plt.plot(test, label='Actual Prices')
plt.plot(forecast, color='red', label='Forecasted Prices')
plt.title(f'{currency} Shared Price Forecast using ARIMA')
plt.xlabel('Time')
plt.ylabel(f'{currency} Shared Price')
plt.legend()
plt.show()

# Calculate performance metrics
mae = mean_absolute_error(test, forecast)
rmse = mean_squared_error(test, forecast, squared=False)
r2 = r2_score(test, forecast)

print(f"Mean Absolute Error (MAE): ${mae:.2f}")
print(f"Root Mean Square Error (RMSE): ${rmse:.2f}")
print(f"R2 Score: {r2:.2f}")
