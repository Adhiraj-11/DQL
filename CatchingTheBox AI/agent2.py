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

class Agent:
    def __init__(self):
        self.n_game = 0
        self.epsilon = 0 # Randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = linear_qnet(5,256,2) 
        self.trainer = Qtrainer(self.model,lr=LR,gamma=self.gamma)

    def get_state(self,game):

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT

        dist = game.paddle_x - game.box.x

        state = [
            # Move Direction
            dir_l,
            dir_r,

            #distance between the paddle and the ball in horizontal axis
            dist,

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

    def get_action(self,state):
        # random moves: tradeoff explotation / exploitation
        self.epsilon = 80 - self.n_game
        final_move = [0,0]
        if(random.randint(0,200)<self.epsilon):
            move = random.randint(0,1)
            final_move[move]= 1
        else:
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0) # prediction by model 
            move = torch.argmax(prediction).item()
            final_move[move]=1 
        return final_move



def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = BOX()
    while True:
        
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        agent.train_short_memory(state_old,final_move,reward,state_new,done)
        agent.remember(state_old,final_move,reward,state_new,done)
        

        if done:
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