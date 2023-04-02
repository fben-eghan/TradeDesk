import numpy as np
import scipy.stats as stats

# Define portfolio characteristics
portfolio_value = 1000000
asset_values = np.array([500000, 500000])
correlation_matrix = np.array([[1, 0.8], [0.8, 1]])
volatility_matrix = np.array([[0.2, 0.1], [0.1, 0.15]])
time_horizon = 1  # in years
num_simulations = 10000

# Define VaR and ES confidence levels
var_confidence_level = 0.95
es_confidence_level = 0.975

# Simulate future returns
mean_returns = np.log(asset_values) - 0.5 * np.diag(volatility_matrix) ** 2
cholesky_decomposition = np.linalg.cholesky(correlation_matrix.dot(volatility_matrix).dot(correlation_matrix))
normal_returns = np.random.normal(size=(num_simulations, 2))
log_returns = mean_returns + cholesky_decomposition.dot(normal_returns.T).T
portfolio_returns = portfolio_value * np.sum(np.exp(log_returns) - 1, axis=1)

# Calculate VaR and ES
var_95 = np.percentile(portfolio_returns, 100 * (1 - var_confidence_level))
es_975 = np.mean(np.sort(portfolio_returns)[:int(num_simulations * es_confidence_level)])

# Print results
print(f"The 95% VaR is {var_95:.2f}")
print(f"The 97.5% ES is {es_975:.2f}")
