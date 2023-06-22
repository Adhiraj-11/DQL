import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set up the game window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Catch The Box")

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


clock = pygame.time.Clock()


running = True
while running:
   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < window_width - paddle_width:
        paddle_x += paddle_speed

   
    object_y += object_speed

  
    if (
        object_y + object_height >= paddle_y
        and paddle_x <= object_x + object_width <= paddle_x + paddle_width
    ):
    
        object_x = random.randint(0, window_width - object_width)
        object_y = 0


    if object_y + object_height >= window_height:

        object_x = random.randint(0, window_width - object_width)
        object_y = 0


    window.fill(BLACK)

    pygame.draw.rect(window, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

    
    pygame.draw.rect(window, WHITE, (object_x, object_y, object_width, object_height))

    
    pygame.display.flip()

    
    clock.tick(60)


pygame.quit()
