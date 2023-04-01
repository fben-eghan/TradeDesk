"""
This code downloads historical stock prices for Apple from Yahoo Finance,calculates the daily returns,
and uses mean-variance portfolio optimization to find the optimal portfolio weights that maximize the Sharpe ratio (the ratio of expected return to expected volatility).
It then plots the efficient frontier of portfolios for a range of expected returns.
"""
import numpy as np
import pandas as pd
import scipy.optimize as sco
import pandas_datareader as pdr
import matplotlib.pyplot as plt

# Download historical stock prices from Yahoo Finance
prices = pdr.get_data_yahoo('AAPL', start='2010-01-01', end='2022-03-31')

# Calculate daily returns
returns = prices['Adj Close'].pct_change()

# Calculate mean and covariance of returns
mu = returns.mean()
sigma = returns.cov()

# Define the objective function for portfolio optimization
def objective(weights):
    return np.dot(weights, mu) / np.sqrt(np.dot(weights, np.dot(sigma, weights)))

# Set constraints on the weights
cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})

# Set bounds on the weights
bounds = [(0, 1)] * len(mu)

# Find the optimal portfolio weights
opt = sco.minimize(objective, x0=np.ones(len(mu)) / len(mu), method='SLSQP', bounds=bounds, constraints=cons)

# Calculate the expected portfolio return and volatility
ret = np.dot(opt.x, mu)
vol = np.sqrt(np.dot(opt.x, np.dot(sigma, opt.x)))

# Print the results
print('Portfolio weights:', opt.x)
print('Expected portfolio return:', ret)
print('Expected portfolio volatility:', vol)

# Plot the efficient frontier
mus = np.linspace(0, 0.3, 100)
frontier = []
for mu in mus:
    def objective(weights):
        return np.dot(weights, mu) / np.sqrt(np.dot(weights, np.dot(sigma, weights)))
    opt = sco.minimize(objective, x0=np.ones(len(mu)) / len(mu), method='SLSQP', bounds=bounds, constraints=cons)
    frontier.append((mu, np.sqrt(np.dot(opt.x, np.dot(sigma, opt.x))), opt.x))
frontier_df = pd.DataFrame(frontier, columns=['mu', 'vol', 'weights'])
frontier_df.plot(kind='scatter', x='vol', y='mu')
plt.show()
