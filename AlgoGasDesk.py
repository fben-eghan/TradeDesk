import pandas as pd
import numpy as np

# Load historical gas price data
data = pd.read_csv('gas_prices.csv')
data['date'] = pd.to_datetime(data['date'])
data = data.set_index('date')

# Define the trading strategy
class GasTradingStrategy:
    
    def __init__(self, data, ma_period=10, threshold=0.2, trade_amount=1000):
        self.data = data
        self.ma_period = ma_period
        self.threshold = threshold
        self.trade_amount = trade_amount
        
    def backtest(self):
        # Calculate the moving average and standard deviation
        ma = self.data['price'].rolling(window=self.ma_period).mean()
        std = self.data['price'].rolling(window=self.ma_period).std()
        
        # Calculate the z-score of each data point
        z_score = (self.data['price'] - ma) / std
        
        # Enter a long position if the z-score is below the threshold
        if z_score.iloc[-1] < -self.threshold:
            return 'BUY', self.trade_amount
        
        # Exit the long position if the z-score is above the threshold
        elif z_score.iloc[-1] > self.threshold:
            return 'SELL', self.trade_amount
        
        # Do nothing if the z-score is within the threshold
        else:
            return 'HOLD', 0

# Create an instance of the trading strategy
strategy = GasTradingStrategy(data, ma_period=20, threshold=1.5, trade_amount=1000)

# Backtest the strategy on historical data
portfolio_value = 10000
for i in range(len(data)):
    signal, amount = strategy.backtest()
    
    if signal == 'BUY':
        portfolio_value -= amount * data.iloc[i]['price']
        position = amount
        
    elif signal == 'SELL':
        portfolio_value += position * data.iloc[i]['price']
        position = 0
        
    else:
        pass
    
# Print the final portfolio value
print('Final portfolio value: %.2f USD' % portfolio_value)
