import numpy as np
import pdb
from matplotlib import pyplot as plt

T = 1 #time in the future (in years)
N = 100 #number of time steps in the tree
delT = T / N #compute time resolution

r = .05 #risk free rate
sigma = .2 #volatility of asset

u, d = np.exp(sigma*np.sqrt(delT)), np.exp(-sigma*np.sqrt(delT))
S0 = 100
K = 100

option = 'call'

# set up initial price
S = np.zeros((N+1)*(N+2)//2)
S[0] = S0
S[np.cumsum(range(1, N+1))] = S[0]*u**range(1, N+1)
for i in range(len(S)):
    if(S[i] == 0):
        S[i] = S[i-1]*d**2


"""
Set up option payoffs - right now this is only for puts or call options. Will 
extend to more complex options in the future..
"""
optionPrice = np.zeros((N+1)*(N+2)//2)
if option == 'call':
    optionPrice[-N-1:] = np.maximum(S[-N-1:] - K, 0)
elif option == 'put':
    optionPrice[-N-1:] = np.maximum(K - S[-N-1:], 0)

indices = [] # these indices keep track of how far to look ahead in S for the loop
[indices.extend([i]*i) for i in range(N + 1)]

for i in reversed(range(0, N*(N+1)//2)):
    priceUp, priceDn = optionPrice[i + indices[i]], optionPrice[i + indices[i] + 1]
    stockUp, stockDn = S[i + indices[i]], S[i + indices[i] + 1]

    rateUp = np.exp(r*delT)**indices[i]
    repPortfolio = np.matmul(np.linalg.inv([[stockUp, rateUp], 
                            [stockDn, rateUp]]), 
                            np.array([priceUp, priceDn]).T)
    rp = (np.exp(r*delT) - d)/(u - d)
    optionPrice[i] = np.exp(-r*delT)*(rp*optionPrice[i + indices[i]] + (1 - rp)*optionPrice[i + indices[i] + 1])
    # optionPrice[i] = repPortfolio[0]*S[i] + \
    #                         repPortfolio[1]*np.exp(r*delT)**(indices[i] - 1)
pdb.set_trace()
print(f'Price of {option} option: {optionPrice[0]:.4f}')