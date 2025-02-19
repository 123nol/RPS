'''
# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
'''


import numpy as np
import random

def player(prev_play="", opponent_history=[], my_prev=[], q_table=[], my_wins=0, prev_state=[], epsilon=[0.5]):
    l_rate = 0.1
    discount = 0.85
    reward = 0
    
    start_epsilon_decay = 1
    end_epsilon_decay = 500
    epsilon_decay = 0.5 / (end_epsilon_decay - start_epsilon_decay) if end_epsilon_decay - start_epsilon_decay != 0 else 0
    
    ints = {"R": 0, "P": 1, "S": 2}
    strs = {0: "R", 1: "P", 2: "S"}
    
    if prev_play == "":
        my_prev .append(strs[random.randint(0, 2)])
        return my_prev[0]
    
    if not q_table:
        q_table = np.random.uniform(low=-1, high=1, size=(3, 3, 3))
    
    opponent_history.append(prev_play)
    
    # Determine reward based on previous outcome
    if prev_play == my_prev[0]:
        reward = 0    # Tie
        win_state = 1
    elif (my_prev[0] == "P" and prev_play == "R") or \
         (my_prev[0] == "R" and prev_play == "S") or \
         (my_prev[0] == "S" and prev_play == "P"):
        reward = 1    # Win
        win_state = 2
        my_wins += 1
    else:
        reward = -1   # Loss
        win_state = 0
    
    new_state = [ints[prev_play], win_state]
    
    # Update Q-table if enough history exists
    if len(opponent_history) >= 2:
        action_index = ints[my_prev[0]]
        old_q = q_table[tuple(prev_state + [action_index])]
        max_future_q = np.max(q_table[tuple(new_state)])
        new_q = (1 - l_rate) * old_q + l_rate * (reward + discount * max_future_q)
        q_table[tuple(prev_state + [action_index])] = new_q
    
    # Choose next action (epsilon-greedy)
    if np.random.random() > epsilon[0]:
        next_move = strs[np.argmax(q_table[tuple(new_state)])]
    else:
        next_move = strs[random.randint(0, 2)]
    
    # Decay epsilon
    if start_epsilon_decay < len(opponent_history) < end_epsilon_decay:
        epsilon=[epsilon[0] -epsilon_decay]
    
    prev_state = new_state
    my_prev[0] = next_move
    
    return next_move