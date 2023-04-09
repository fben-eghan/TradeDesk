import pandas as pd
import requests
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans

# Load historical gas price data
data = pd.read_csv('gas_prices.csv')
data['date'] = pd.to_datetime(data['date'])
data = data.set_index('date')

# Define the trading strategy
class GasTradingStrategy:
    
    def __init__(self, data):
        self.data = data
        self.position = 0
        
        # Initialize machine learning models
        self.regression_model = LinearRegression()
        self.cluster_model = KMeans(n_clusters=2)
        
    def backtest(self):
        # Get weather forecast data
        city = 'Houston'
        api_key = '1234567890'
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        temp = requests.get(weather_url).json()['main']['temp']
        
        # Get pipeline flow data
        pipeline_url = 'https://api.pipelines.com/v1/flows'
        flow = requests.get(pipeline_url).json()['flows'][0]['flow']
        
        # Calculate the moving average and standard deviation
        ma = self.data['price'].rolling(window=10).mean()
        std = self.data['price'].rolling(window=10).std()
        
        # Calculate the z-score of each data point
        z_score = (self.data['price'] - ma) / std
        
        # Use machine learning models to make predictions
        X = self.data[['price', 'volume']]
        y = self.data['price']
        self.regression_model.fit(X, y)
        self.cluster_model.fit(X)
        trend = self.regression_model.predict(X)[-1]
        cluster = self.cluster_model.predict(X)[-1]
        
        # Enter a long position if conditions are favorable
        if (z_score.iloc[-1] < -0.2) and (trend > self.data['price'].iloc[-1]) and (cluster == 0) and (temp < 50) and (flow > 5000):
            signal = 'BUY'
            amount = 1000
            self.position += amount
            
        # Exit the long position if conditions change
        elif (self.position > 0) and ((z_score.iloc[-1] > 0.2) or (trend < self.data['price'].iloc[-1]) or (cluster == 1) or (temp >= 50) or (flow <= 5000)):
            signal = 'SELL'
            amount = self.position
            self.position = 0
            
        # Do nothing if conditions are not favorable or there is no existing position
        else:
            signal = 'HOLD'
            amount = 0
        
        # Log the trade
        trade_data = {
            'signal': signal,
            'price': self.data['price'].iloc[-1],
            'position': self.position,
            'temp': temp,
            'flow': flow
        }
        return trade_data
