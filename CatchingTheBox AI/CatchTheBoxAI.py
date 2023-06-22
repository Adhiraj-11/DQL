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
    
Point = namedtuple('Point','x,y')
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

score = 0

# Define the falling object properties
# object_width = 20
# object_height = 20
# object_x = random.randint(0, window_width - object_width)
# object_y = 0
box_speed = 3

class BOX:
    def __init__(self,w = window_width,h = window_height):
        self.w = w
        self.h = h

        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("Catch Box Game")
        self.tiktok = pygame.time.Clock() 

        #clock = pygame.time.Clock()

        self.reset()

    def reset(self):
        self.paddle = self.Paddle(paddle_x, paddle_y, paddle_width, paddle_height, paddle_speed)
        self.direction = Direction.RIGHT
        self.score = 0
        self.frame_itteration = 0
        #self.box = None
        self.generate_box()

    def generate_box(self):
        self.box_width = 20
        self.box_height = 20
        box_x = random.randint(0, window_width - self.box_width)
        box_y = 0
        self.box = Point(box_x,box_y)

        if (box_y + self.box_height >= box_y
        and self.paddle_x <= box_x + self.box_width <= self.paddle_x + self.paddle_width):
                self.generate_box()


    def play_step(self,action):
        self.frame_itteration += 1

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()

        self.move(action)

        reward = 0
        game_over = False

        if(self.missed_the_box()):
            game_over = True
            reward = -1
            # self.reset()
            return reward,game_over,self.score
        
        if(self.box.y + self.box_height >= self.paddle_y
        and self.paddle_x <= self.box.x + self.box_width <= self.paddle_x + self.paddle_width):
            self.score += 1
            game_over = False
            reward = 1
            self.generate_box()

        self.update_ui()
        self.tiktok.tick(30)

        return reward,game_over,self.score

    def update_ui(self):
        self.display.fill(black)
        pygame.draw.rect(self.display, red, (self.paddle_x, self.paddle_y, self.paddle_width, self.paddle_height))
        pygame.draw.rect(self.display, green, (self.box.x, self.box.y, self.box_width, self.box_height))
        new_box_y = self.box.y + box_speed
        self.box = self.box._replace(y=new_box_y)  # Update the y attribute
        text = font.render("Score: "+str(self.score),True,blue)
        self.display.blit(text,[0,0])
        pygame.display.flip()

    def move(self,action):
        clock_wise = [Direction.RIGHT,Direction.LEFT]

        idx = clock_wise.index(self.direction)

        if np.array_equal(action,[1,0]):
            new_dir = clock_wise[idx]
        else:
            next_idx = (idx - 1) % 2
            new_dir = clock_wise[next_idx] 
        self.direction = new_dir

        
        if(self.direction == Direction.RIGHT and self.paddle_x < window_width - paddle_width):
            self.paddle_x += paddle_speed
        elif(self.direction == Direction.LEFT and self.paddle_x > 0):
            self.paddle_x -= paddle_speed
        
        
    def Paddle(self,x,y,w,h,speed):
        self.paddle_x = x
        self.paddle_y = y
        self.paddle_width = w
        self.paddle_height = h
        self.Paddle_speed = speed


    def missed_the_box(self):
        if self.box.y + self.box_height >= window_height:
            return True
       
        return False

        
            
