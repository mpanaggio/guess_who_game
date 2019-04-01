# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 07:47:33 2019

@author: mjpbb
"""
# import packages
import numpy as np
import guess_who_game as gw

#%% Generate sample strategy
bmat=np.zeros((24,24))
for my_rem in range(1,25):
    for their_rem in range(1,25):
        bmat[my_rem-1,their_rem-1]=max(int(np.floor(my_rem/2)),1)
#print(bmat)


#%% select strategies
#strategy1={'type':'fixed_p','p':0.5}
strategy1={'type':'matrix','bmat':bmat}
#strategy1={'type':'random','b':3}
strategy2={'type':'fixed_b','b':5}

#%% simulate game
winner,b1,b2=gw.play_game(strategy1,strategy2,return_b=True)
print("Winner:", winner)
print("Player 1 guesses:",b1)
print("Player 2 guesses:",b2)