import scipy.stats as stats

# Define portfolio returns
portfolio_returns = [-0.02, 0.01, -0.03, 0.02, 0.005, -0.01, 0.02, -0.01, 0.015, 0.02]

# Calculate the 95% VaR
var_95 = stats.norm.ppf(0.05, loc=np.mean(portfolio_returns), scale=np.std(portfolio_returns))

# Print the VaR
print(f"The 95% VaR is {var_95:.3f}")



# Define threshold
threshold = np.percentile(portfolio_returns, 5)

# Calculate the ES
es = np.mean([loss for loss in portfolio_returns if loss <= threshold])

# Print the ES
print(f"The ES is {es:.3f}")


# Define threshold
threshold = np.percentile(portfolio_returns, 5)

# Calculate the CVaR
cvar = np.mean([loss for loss in portfolio_returns if loss <= threshold]) + 0.5 * np.mean([loss for loss in portfolio_returns if loss > threshold])

# Print the CVaR
print(f"The CVaR is {cvar:.3f}")

