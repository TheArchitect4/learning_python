import math 
import pygame
import random
from itertools import combinations
import time
from bluepriunt import *
pygame.init()

screen_width = 1600
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Time
fps_of_game = 60
sub_steps = 6




star_list = []
number_of_stars = int((screen_width * screen_height)) // 5000
for star in range(number_of_stars):
    rand_x = random.randint(0, screen_width)
    rand_y = random.randint(0, screen_height)
    star_list.append((rand_x, rand_y))


bodies = [
    # 1. The Central Star (Fixed massive anchor)
    Body(mass=2000000, radius=35, x=800, y=500, vx=0, vy=0, color=(255, 220, 50), fixed=True),
    
    # 2. Inner Planet (Fast orbit)
    #Body(mass=1000, radius=8, x=600, y=500, vx=0, vy=3.2,  color=(0, 150, 255)),
    
    # 3. Outer Planet (Slower, wider orbit)
    #Body(mass=3000, radius=14, x=500, y=500, vx=0, vy=2.1, color=(200, 100, 50)),
]

### creatig 50 sattelies around the center planet
for _ in range(200):
    sx = bodies[0].x
    sy = bodies[0].y
    r = random.uniform(150, 400)
    angle = random.uniform(0, 2 * math.pi)
    speed = math.sqrt((Gravitational_constant * bodies[0].mass) / r)
    #position of sun(sx,sy) plus rcos, rsin -- polar coordinates
    x = sx + r * math.cos(angle)
    y = sy + r * math.sin(angle)
    ### when we differentiate those polar coords we get a formula for the velocity at that point which is perpendicular to r
    vx = -speed * math.sin(angle)
    vy = speed * math.cos(angle)
    bodies.append(Body(mass=1, radius=5, x=x, y=y, vx=vx, vy=vy, color=(0, 150, 255)))

while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

    screen.fill((30, 30, 30))
    
    frame_dt = clock.tick(fps_of_game) / 1000.0
    sub_dt = frame_dt / sub_steps

    ### Physics sub stepping calculations -- basically important physics calculations and boundary calculations 8 times per tick
    for _ in range(sub_steps):
        
        # Reset Forces
        for body in bodies:
            body.reset_forces()
  
        # Gravity
        for body1, body2  in combinations(bodies, 2):

            body1.attract(body2)
            body1.colide(body2)
  
        # Integrate
        for body in bodies: 
            body.integration(sub_dt, screen_width, screen_height)
        

    # Drawing everything
    for _ in star_list:

        pygame.draw.circle(screen, (255, 255, 255), (_), 1)
    for body in bodies:
        body.draw(screen)

    font = pygame.font.SysFont(None, 28)

    # in the loop
    fps_text = font.render(f"FPS: {clock.get_fps():.1f}  bodies: {len(bodies)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))


    # Update the display
    pygame.display.flip() 

    clock.tick(fps_of_game)

pygame.quit()

