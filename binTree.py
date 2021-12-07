import numpy as np
import pdb

T = .1 #time in the future (in years)
N = 5 #number of time steps in the tree
delT = T / N #compute time resolution

r = .05 #risk free rate
sigma = .2 #volatility of asset

u, d = np.exp(sigma*np.sqrt(delT)), np.exp(-sigma*np.sqrt(delT))
S0 = 100
K = 100

option = 'call'

# set up initial price
S = np.zeros(N*(N+1)//2)
S[0] = S0
S[np.cumsum(range(1, N))] = S[0]*u**range(1, N)
for i in range(len(S)):
    if(S[i] == 0):
        S[i] = S[i-1]*d**2


"""
Set up option payoffs - right now this is only for puts or call options. Will 
extend to more complex options in the future..
"""
optionPrice = np.zeros(N*(N+1)//2)
if option == 'call':
    optionPrice[-N:] = np.maximum(S[-N:] - K, 0)
elif option == 'put':
    optionPrice[-N:] = np.maximum(K - S[-N:], 0)

indices = []
[indices.extend([i]*i) for i in range(N)]
for i in reversed(range(0, N*(N-1)//2)):
    priceUp, priceDn = optionPrice[i + indices[i]], optionPrice[i + indices[i]]
    stockUp, stockDn = S[i + indices[i]], S[i + indices[i] + 1]
    rateUp = np.exp(1 + r)**indices[i]

    repPortfolio = np.matmul(np.linalg.inv([[stockUp, rateUp], 
                            [stockDn, rateUp]]), 
                            np.array([priceUp, priceDn]).T)

    optionPrice[i] = repPortfolio[0]*S[i] + \
                            repPortfolio[1]*np.exp(1 + r)**(indices[i] - 1)
    
print(f'Price of {option} option: {optionPrice[0]:.4f}')