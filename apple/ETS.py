import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import datetime as dt
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Fetch data from yfinance
currency = 'AAL'
start = dt.datetime(2020, 1, 1)
end = dt.datetime(2023, 7, 1)
data = yf.Ticker(currency).history(start=start, end=end)

# Splitting the data into train and test
train = data['Close'].iloc[:-60]
test = data['Close'].iloc[-60:]

# Applying Exponential Smoothing
model = ExponentialSmoothing(train, trend='add', seasonal='add', seasonal_periods=365)
fit = model.fit()

# Making predictions
predictions = fit.forecast(steps=60)

# Plot the results
plt.figure(figsize=(15,6))
plt.plot(train, label='Train')
plt.plot(test, label='Test')
plt.plot(test.index, predictions, label='Predicted')
plt.legend()
plt.title(f"{currency} Shared Price Forecast with ETS")
plt.show()

# Calculating metrics
mae = mean_absolute_error(test, predictions)
rmse = mean_squared_error(test, predictions, squared=False)
r2 = r2_score(test, predictions)

print(f"Mean Absolute Error (MAE): ${mae:.2f}")
print(f"Root Mean Square Error (RMSE): ${rmse:.2f}")
print(f"R2 Score: {r2:.2f}")
