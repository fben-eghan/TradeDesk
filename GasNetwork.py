import networkx as nx

# Create an empty graph
G = nx.Graph()

# Add nodes for gas supply sources
G.add_node('Natural Gas Wells', type='Supply', location='Various', capacity=100, cost=2.50)
G.add_node('LNG Terminals', type='Supply', location='Various', capacity=50, cost=3.00)
G.add_node('Pipeline Interconnects', type='Supply', location='Various', capacity=75, cost=2.75)

# Add nodes for gas demand sources
G.add_node('Power Plants', type='Demand', location='Various', consumption=75, demand='Base Load')
G.add_node('Industrial Facilities', type='Demand', location='Various', consumption=25, demand='Flexible')
G.add_node('Residential Consumers', type='Demand', location='Various', consumption=10, demand='Stable')

# Add nodes for gas transmission infrastructure
G.add_node('Transmission Pipelines', type='Infrastructure', location='Various', capacity=200, pressure=150)
G.add_node('Compressor Stations', type='Infrastructure', location='Various', capacity=100, pressure=200)

# Add nodes for gas contracts
G.add_node('Contract A', type='Contract', volume=50, duration='1 year', price=3.00)
G.add_node('Contract B', type='Contract', volume=25, duration='6 months', price=3.25)
G.add_node('Contract C', type='Contract', volume=100, duration='2 years', price=2.75)

# Add nodes for trading strategies
G.add_node('Long-Term Contracts', type='Strategy', risk='Low', profitability='Medium', market_outlook='Stable')
G.add_node('Short-Term Contracts', type='Strategy', risk='High', profitability='High', market_outlook='Volatile')

# Add nodes for market data sources
G.add_node('Natural Gas Futures', type='Market Data', source='CME Group', frequency='Daily', reliability='High')
G.add_node('Natural Gas Spot Prices', type='Market Data', source='EIA', frequency='Weekly', reliability='Medium')

# Add edges to represent relationships between nodes
G.add_edge('Natural Gas Wells', 'Transmission Pipelines', flow=100)
G.add_edge('LNG Terminals', 'Transmission Pipelines', flow=50)
G.add_edge('Pipeline Interconnects', 'Transmission Pipelines', flow=75)
G.add_edge('Transmission Pipelines', 'Power Plants', flow=60)
G.add_edge('Transmission Pipelines', 'Industrial Facilities', flow=30)
G.add_edge('Transmission Pipelines', 'Residential Consumers', flow=10)
G.add_edge('Transmission Pipelines', 'Compressor Stations')
G.add_edge('Compressor Stations', 'Transmission Pipelines')
G.add_edge('Power Plants', 'Contract A')
G.add_edge('Industrial Facilities', 'Contract B')
G.add_edge('Residential Consumers', 'Contract C')
G.add_edge('Long-Term Contracts', 'Natural Gas Futures')
G.add_edge('Short-Term Contracts', 'Natural Gas Spot Prices')

# Print the nodes and edges of the graph
print(G.nodes(data=True))
print(G.edges(data=True))
