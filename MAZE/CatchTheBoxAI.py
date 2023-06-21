import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

font = pygame.font.SysFont("none", 30)
score_font = pygame.font.SysFont("comicsansms", 20)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    

blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

window_width = 800
window_height = 600

# Define the paddle properties
paddle_width = 50
paddle_height = 10
paddle_x = window_width // 2 - paddle_width // 2
paddle_y = window_height - 50
paddle_speed = 5

# Define the falling object properties
object_width = 20
object_height = 20
object_x = random.randint(0, window_width - object_width)
object_y = 0
object_speed = 3

class BOX:
    def __init__(self,w = window_width,h = window_height):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("Catch Box Game")

        clock = pygame.time.Clock()

        self.reset()
    def reset(self):

        self.direction = Direction.RIGHT
        self.score = 0
        self.fram_itteration = 0
    
    def move(self,action):
        
        clock_wise = [Direction.RIGHT,Direction.LEFT]

        idx = clock_wise.index(self.direction)

        if np.array_equal(action,[1,0]):
            new_dir = clock_wise[idx]
        else:
            next_idx = (idx - 1) % 2
            new_dir = clock_wise[next_idx] 
        self.direction = new_dir

        
        if(self.direction == Direction.RIGHT):
            paddle_x += paddle_speed
        elif(self.direction == Direction.LEFT):
            paddle_x -= paddle_speed
        

