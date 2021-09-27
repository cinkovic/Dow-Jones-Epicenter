'''needs to be implemented inside Jupyter Notebook in order to yield a picture
Takes few minutes to process..
'''

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import yfinance as yf

var1 = yf.Ticker('AAPL')
apple = var1.institutional_holders
apple['comp'] = var1.ticker

var2 = yf.Ticker('MSFT')
microsoft = var2.institutional_holders
microsoft['comp'] = var2.ticker
var3 = yf.Ticker('GOOGL')
google = var3.institutional_holders
google['comp'] = var3.ticker
# google
# microsoft
# apple

together_ = pd.concat([apple, google, microsoft])
# together_.sort_values('Value', ascending=False)
# together_.sort_values('Holder', ascending=False)

G = nx.from_pandas_edgelist(together_, 'Holder', 'comp')
# G.nodes()
# nx.draw(G, with_labels=True)

tickers = pd.read_html('https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average')[1]

tickers = tickers.Symbol.to_list()

frames = []

for ticker in tickers:
    var = yf.Ticker(ticker)
    frame = var.institutional_holders
    frame['comp'] = var.ticker
    frames.append(frame)

all_together = pd.concat(frames)
# all_together

G = nx.from_pandas_edgelist(all_together, 'Holder', 'comp', edge_attr=True)

edgelist = nx.to_edgelist(G)
# edgelist
nodewidth = [round(v[2]['Value'] / 50_000_000_000,1) for v in edgelist]
# nodewidth = [v[2]['Value'] for v in edgelist]
# nodewidth

colors = []
for node in G:
    if node in all_together['comp'].values:
        colors.append('red')
    else:
        colors.append('blue')
        
# G.degree()
nodesize = [v * 100 for v in dict(G.degree()).values()]

plt.figure(figsize=(50,40)) #change size
# plt.figure(figsize=(30,25))
nx.draw(G, with_labels=True, 
        node_color=colors, 
        node_size=nodesize, 
        width=nodewidth
       )
ax = plt.gca()
ax.collections[0].set_edgecolor('#696969')
