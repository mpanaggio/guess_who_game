# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 07:32:37 2019

@author: mjpbb
"""
import numpy as np

def initialize_game():
    ''' initialize variables describing state of the game'''
    remaining_1=24
    remaining_2=24
    turn=1
    return remaining_1,remaining_2,turn
def make_guess(remaining,b):    
    ''' given the number of candidates (remaining) and the number of yes answers to the question (b), flip 
    a coin to determine if the answer is yes or no and then update the number of remaining candidates.'''
    prob_true=b/remaining
    prob_false=1-prob_true
    result=np.random.choice([True,False],p=[prob_true,prob_false])
    if result: # Yes
        remaining=b
    else: # No
        remaining=remaining-b
    return remaining
def update_state(remaining_1,remaining_2,turn,b):
    '''Given the current state and the question to ask with number of yes answers (b), update the state.'''
    if turn==1:
        remaining_1=make_guess(remaining_1,b)
    else:
        remaining_2=make_guess(remaining_2,b)
    return remaining_1,remaining_2,3-turn

def choose_b(yours,opponents,strategy):
    ''' Given the state of the system and the strategy, determine which question to ask, i.e. how many 
    yes answers should there be? (b)'''
    if strategy['type']=='fixed_p': # b=p*remaining
        b=int(np.round(strategy['p']*yours))
    elif strategy['type']=='fixed_b': # b is fixed
        b=int(strategy['b'])
    elif strategy['type']=='random': # b is uniform and random
        try:
            b=np.random.choice(range(1,yours),p=strategy['p'][yours,opponents,:])
        except:
            b=np.random.choice(range(1,yours))
    elif strategy['type']=='matrix':
        bmat=strategy['bmat']
        b=bmat[yours-1,opponents-1]
    b=max(min(b,yours-1),1) # make it an integer
    
    return int(b)

def play_game(strategy1,strategy2,return_b=False):
    ''' Simulate a single game and return the winner and the guesses at each state along the way'''
    remaining_1,remaining_2,turn=initialize_game()
    print("Initial state:", "rem1:",remaining_1,"rem2:",remaining_2,"turn:",turn)
    b1=[]
    b2=[]
    while min(remaining_1,remaining_2)>1:
        if turn==1:
            b=choose_b(yours=remaining_1,opponents=remaining_2,strategy=strategy1)
            b1.append((remaining_1,remaining_2,b))
        else:
            b=choose_b(yours=remaining_2,opponents=remaining_1,strategy=strategy2)
            b2.append((remaining_2,remaining_1,b))
        remaining_1,remaining_2,turn=update_state(remaining_1,remaining_2,turn,b)
        print("new state:", "rem1:",remaining_1,"rem2:",remaining_2,"turn:",turn)
    if remaining_1==1:
        winner=1
    else:
        winner=2
    if return_b:
        return winner,b1,b2
    return winner