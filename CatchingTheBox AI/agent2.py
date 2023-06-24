import numpy as np
import torch
import pygame
from collections import deque
import random
from CatchTheBoxAI import BOX,Direction
from model import linear_qnet, Qtrainer

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001
class RandomNumberGenerator:
    def __init__(self):
        self.previous_number = None
        self.count = 0

    def generate_same_number(self):
        
        if self.count == 0:
            self.previous_number = random.randint(0, 2)
            self.count = 5
            
        self.count -= 1
        return self.previous_number

class Agent:
    def __init__(self):
        self.rng = RandomNumberGenerator()
        self.n_game = 0
        self.epsilon = 0 # Randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = linear_qnet(13,256,3) 
        self.trainer = Qtrainer(self.model,lr=LR,gamma=self.gamma)

    def get_state(self,game):

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT #HERE
        dir_s = game.direction == Direction.STAND
        paddle_speed = 5
        box_speed = 3
        # paddle_center = game.paddle_x + game.paddle_width // 2
        # box_center = game.box.x + game.box_width // 2 

        # dist_x = abs(paddle_center - box_center)

        dist_x = abs(game.paddle_x - game.box.x)
        dist_y = game.paddle_y - game.box.y
        paddle_x = game.paddle_x
        box_x = game.box.x
        dist_diag = np.sqrt(dist_x**2 + dist_y**2)
        
        max_distance = np.sqrt(game.w**2 + game.h**2)

        # Set the proximity threshold as a fraction of the max distance
        proximity_threshold = 0.1 * max_distance  # Adjust the fraction as needed
        proximity = 0
        if dist_diag <= proximity_threshold:
            proximity = 1
        allignment = 0
        if dist_x <= 10:
            allignment = 1

        state = [
            # Move Direction
            dir_l,
            dir_r,
            dir_s,

            paddle_x,
            box_x,

            #distance between the paddle and the ball in horizontal axis
            dist_x,
            dist_y,
            dist_diag,
            

            allignment,

            paddle_speed,
            box_speed,

            game.box.x < game.paddle_x, # box is in left
            game.box.x > game.paddle_x, # box is in right
            ]
        
        return np.array(state,dtype=int)


    def remember(self,state,action,reward,next_state,done):
        self.memory.append((state,action,reward,next_state,done)) # popleft if memory exceed

    def train_long_memory(self):
        if (len(self.memory) > BATCH_SIZE):
            mini_sample = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_sample = self.memory
        states,actions,rewards,next_states,dones = zip(*mini_sample)
        self.trainer.train_step(states,actions,rewards,next_states,dones)

    def train_short_memory(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)

    
    
    
    def get_action(self,state): #HERE
        # random moves: tradeoff explotation / exploitation
        #self.epsilon = 500- self.n_game * 2  # Higher initial epsilon value
        #final_move = [0, 0, 0]
        self.epsilon = 80 - self.n_game
        final_move = [0,0,0]
        if(random.randint(0,200)<self.epsilon):
        #if(self.epsilon > 0):
            
            move = self.rng.generate_same_number() #random.randint(0,2)
            # print(self.rng.count)
            # print(move)
            final_move[move]= 1
            
        else:
            # print("prediction")
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0) # prediction by model 
            move = torch.argmax(prediction).item()
            final_move[move]=1 
        return final_move

    
        

def train():
    record = 0
    agent = Agent()
    game = BOX()
    while True:
        # print(game.paddle_x)
        # print(game.box.x)
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old,final_move,reward,state_new,done)
        agent.remember(state_old,final_move,reward,state_new,done)
        #print(state_old)
        

        if done:
            #print(state_old)
            game.reset()
            agent.n_game += 1
            agent.train_long_memory()
            if(score > record): 
                record = score
                agent.model.save()
            print('Game:',agent.n_game,'Score:',score,'Record:',record)
            
            # plot_scores.append(score)
            # total_score+=score
            # mean_score = total_score / agent.n_game
            # plot_mean_scores.append(mean_score)
            # plot(plot_scores,plot_mean_scores)


if(__name__=="__main__"):
    train()