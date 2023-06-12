import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
import math
pygame.init()

font = pygame.font.SysFont("none", 30)
score_font = pygame.font.SysFont("comicsansms", 20)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
 
Point = namedtuple('Point','x,y')

blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

lambai = 300
chodai = 300
x1 = lambai / 2
y1 = chodai / 2 
BLOCK_SIZE = 10
score = 0
saanp = 10
saanp_ki_tezi = 10

class SnakeAI:
    def __init__(self,w=chodai,h=lambai):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("SAANP KA KHEL ")

        self.tiktok = pygame.time.Clock() 

        self.reset()
    def reset(self):

        self.direction = Direction.RIGHT
        self.head = Point(x1,y1)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE,self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]
        
        self.score = 0
        self.food = None

        self.khaana()
        self.frame_iteration = 0

    def khaana(self):
        #doubt
        x_food = random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y_food = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x_food,y_food)
        if(self.food in self.snake):
            self.khaana()

    def play_step(self,action):
        self.frame_iteration += 1

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()

        self.move(action)
        self.snake.insert(0,self.head)

        reward = 0
        haar_gye_aap = False
        #doubt

        if(self.is_collision() or self.frame_iteration > 100*len(self.snake)):
            haar_gye_aap = True
            reward = -1
            return reward,haar_gye_aap,self.score
        
        if(self.head == self.food):
            self.score += 1
            reward = 1
            self.khaana()

        else:
            #reward = -1
            self.snake.pop()
            

        self.update_ui()
        self.tiktok.tick(saanp_ki_tezi)

        return reward,haar_gye_aap,self.score
    
    def update_ui(self):
        self.display.fill(black)
        for pt in self.snake:
            #doubt
            pygame.draw.rect(self.display,blue,pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            # pygame.draw.rect(self.display,blue,pygame.Rect(pt.x+4,pt.y+4,12,12))
        pygame.draw.rect(self.display,green,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        text = font.render("Score: "+str(self.score),True,red)
        self.display.blit(text,[0,0])
        pygame.display.flip()

    def move(self,action):
        
        clock_wise = [Direction.RIGHT,Direction.DOWN,Direction.LEFT,Direction.UP]
        idx = clock_wise.index(self.direction)
        if np.array_equal(action,[1,0,0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action,[0,1,0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right Turn
        else:
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # Left Turn
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if(self.direction == Direction.RIGHT):
            x+=BLOCK_SIZE
        elif(self.direction == Direction.LEFT):
            x-=BLOCK_SIZE
        elif(self.direction == Direction.DOWN):
            y+=BLOCK_SIZE
        elif(self.direction == Direction.UP):
            y-=BLOCK_SIZE
        self.head = Point(x,y)

    def is_collision(self,pt=None):
        if(pt is None):
            pt = self.head
        #hit boundary
        if(pt.x>self.w-BLOCK_SIZE or pt.x<0 or pt.y>self.h - BLOCK_SIZE or pt.y<0):
            return True
        if(pt in self.snake[1:]):
            return True
        return False