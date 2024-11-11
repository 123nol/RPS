# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.
import numpy as np
import random




def player(prev_play="", opponent_history=[],my_prev="",q_table=[],my_wins=0,prev_state=()):


    l_rate=0.1;
    discount=0.85;
    epislon=0.5;
    reward=0
    start_epislon=1
    #at half the total number of matches.
    end_epislon=500
    epislon_decay=epislon//(end_epislon-start_epislon)
    
    
    
    ints={
        'R':0,
        'P':1,
        'S':2

    }
    strs={
        0:'R',
        1:'P',
        2:'S'
    }
    
        #-2:loss.....1:winrate>=0.6 at defined intervals
    
    if prev_play=="":
        my_prev= strs[random.randint(0,2)]
        return my_prev
    
    if(q_table==[]):
        q_table==np.random.uniform(low=-2,high=1,size=(3,3,3)) 
        


   

    opponent_history.append(prev_play)
    
    if prev_play == my_prev:
            
            reward=-1
            win_state=1
            
    elif (my_prev == "P" and prev_play == "R") or (my_prev == "R" and prev_play == "S") or (my_prev == "S" and prev_play == "P"):
            reward=0
            win_state=2
            my_wins+=1
            
    elif prev_play == "P" and my_prev == "R" or prev_play == "R" and my_prev == "S" or prev_play == "S" and my_prev == "P":
            
           reward=-2
           win_state=0
           
    # if(opponent_history!=[] and len(opponent_history)%100==0 and my_wins/len(opponent_history)>=0.6):
            
    #     reward=1
    
    new_state=tuple((ints[prev_play],win_state))

    
    
    if(len(opponent_history)>=2):
        #training would only start by the time we are about to make our third move, because the first move is random and not based on Q-values, our second move is #technically our first model based move so we dont have the previous state before we made our first move to update the qvalue for.
        
       
        new_Qvalue=(1-l_rate)*q_table[prev_state+(ints[my_prev],)] + l_rate*(reward+discount*np.max(q_table[new_state]))
        q_table[prev_state+(ints[my_prev],)]=new_Qvalue
    if(len(opponent_history)%1000==0 and my_wins/len(opponent_history)>=0.6):

        q_table[prev_state+(ints[my_prev],)]=1
    
    
    next_move=strs[np.argmax(q_table[new_state])] if np.random.random()>epislon else random.randint(0,2)

    prev_state=new_state
    my_prev=next_move
    
    if len(opponent_history)>start_epislon and len(opponent_history)<end_epislon:
         epislon-=epislon_decay
        
    
    

   
    return next_move



    #return strs[next_move] 
 
   
    
    

    # opponent_history.append(prev_play)

    # guess = "R"
    # ''' if(len(opponent_history)%100==0):
    #         if( my_wins/len(opponent_history)<):

    # '''
    # if len(opponent_history) > 2:
    #     guess = opponent_history[-2]

    # return guess
