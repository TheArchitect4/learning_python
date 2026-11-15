import math 
import pygame
import random
from itertools import combinations
pygame.init()

screen_width = 1600
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True



fps_of_game = 60
sub_steps = 8
dt = 1 / sub_steps
Gravitational_constant = 0.8
bounciness = 0.8
planet_trail = []
star_list = []

### Creating a dictionary of objects
bodies = [
    
    {
        "mass": 100,
        "radius": 50,
        "x": 1400,
        "y": 500,
        "velocity_x": 6,
        "velocity_y": 7.38,##6.28 orbit
        "Resultant_force_x": 0,
        "Resultant_force_y": 0,
        "color": (0, 0, 255)
    
    }, 
    {
        "mass": 100000,
        "radius": 100,
        "x": screen_width // 2,
        "y":  screen_height // 2,
        "velocity_x": 0,
        "velocity_y": 0,
        "Resultant_force_x": 0,
        "Resultant_force_y": 0,
        "color": (255, 255, 0)
    },
    {
        "mass": 100,
        "radius": 50,
        "x": 100,
        "y":  100,
        "velocity_x": 6,
        "velocity_y": 0,
        "Resultant_force_x": 0,
        "Resultant_force_y": 0,
        "color": (255, 0, 100)
    }
]











### picking random pixels on the screen and adding it to a list, to then draw in the game loop. we need to generate random numbers in rage 0 to screen width for x
### how many pixels are there, and how many stars we want based on that

number_of_stars = int((screen_width * screen_height)) // 5000

### Then i need to get number of starts many coordinante pairs and put that in a list

for star in range(number_of_stars):
    rand_x = random.randint(0, screen_width)
    rand_y = random.randint(0, screen_height)
    star_list.append((rand_x, rand_y))
    









while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False

    screen.fill((0, 0, 0)) 
    




### Physics sub stepping calculations -- basically important physics calculations and boundary calculations 8 times per tick
    for _ in range(sub_steps):
        
        for body in bodies:
            body["Resultant_force_x"] = 0
            body["Resultant_force_y"] = 0
            ### Calcu gravitational interaction with each pair of bodies, and add it to a resultant force --- store for calculation. combonation saves us here from counting and adding for forces for say mars - earch and earth - mars interaction. so as we go through the list, itll add each EM ES SUM (E=earch, S=Sun, M=Mars) forces and get a total resultant force for each body, from that we can then calculate the velocitry 
        for body1, body2  in combinations(bodies, 2):

            dx = body1["x"] - body2["x"]
            dy = body1["y"] - body2["y"]
            distance_between_bodies = math.hypot(dx, dy)
            if distance_between_bodies == 0:
                distance_between_bodies = 0.001

            gravitational_force = Gravitational_constant * body1["mass"] * body2["mass"] / ((distance_between_bodies) ** 2 + 1)
            ### Fcosx=F_x
            ### fsinx=F_y
            gravitational_force_x = -gravitational_force * (dx / distance_between_bodies)
            gravitational_force_y = -gravitational_force * (dy / distance_between_bodies)

            
            body1["Resultant_force_x"] += gravitational_force_x
            body1["Resultant_force_y"] += gravitational_force_y

            ### Equal and opposite forces
            body2["Resultant_force_x"] += -gravitational_force_x
            body2["Resultant_force_y"] += -gravitational_force_y



            if distance_between_bodies <= body1["radius"] + body2["radius"]:

                overlap = (body1["radius"] + body2["radius"]) - distance_between_bodies + 0.05
                total_mass = body1["mass"] + body2["mass"]

                norm_x = dx / distance_between_bodies
                norm_y = dy / distance_between_bodies
                
                
                ### Find the norm of the direction vector, 1/d (dx, dy) 
                ### this is a clap to provent the balls from merging, and we move them scaled by each of their masses, so the big one doesnt get tp'd by the small one

                body1["x"] += +norm_x * overlap * (body2["mass"] / total_mass) 
                body1["y"] += +norm_y * overlap * (body2["mass"] / total_mass) 

                
                body2["x"] += -norm_x * overlap * (body1["mass"] / total_mass)
                body2["y"] += -norm_y * overlap * (body1["mass"] / total_mass) 


                ### Relative velocity between bodies
                relative_v_x = body1["velocity_x"] - body2["velocity_x"]
                relative_v_y = body1["velocity_y"] - body2["velocity_y"]
                # Find speed along norm -- dot product
                velocity_along_norm = (norm_x * relative_v_x) + (norm_y * relative_v_y)


                if velocity_along_norm < 0:

                    mass_factor = (1 / body1["mass"]) + (1 / body2["mass"])

                    impulse = -(1 + bounciness) * velocity_along_norm / mass_factor
                        
                    
                    body1["velocity_x"] += impulse * (1 / body1["mass"]) * norm_x
                    body1["velocity_y"] += impulse * (1 / body1["mass"]) * norm_y

                    body2["velocity_x"] -= impulse * (1 / body2["mass"]) * norm_x
                    body2["velocity_y"] -= impulse * (1 / body2["mass"]) * norm_y

              




        for body in bodies:
            ### v=u+at a=f/m
            body["velocity_x"] = body["velocity_x"] + ((body["Resultant_force_x"] / body["mass"]) * dt)
            body["velocity_y"] = body["velocity_y"] + ((body["Resultant_force_y"] / body["mass"]) * dt)

            ### somehow stumbled onto the right method for this???  update velocity then position produces a stable orbit, but position then velocity gives me a spiral, learning more about why this happens --- semi-implicit Euler algorith 

            body["x"] = body["x"] + body["velocity_x"] * dt
            body["y"] = body["y"] + body["velocity_y"] * dt

            
            if body["x"] - body["radius"] < 0 or body["x"] + body["radius"] > screen_width:
                body["x"] = max(body["radius"], min(body["x"], screen_width - body["radius"]))
                body["velocity_x"] = -body["velocity_x"] #* 0.8
            
            if body["y"] - body["radius"] < 0 or body["y"] + body["radius"] > screen_height:
                body["y"] = max(body["radius"], min(body["y"], screen_height - body["radius"]))
                body["velocity_y"] = -body["velocity_y"] #* 0.8            
            


    for _ in star_list:
        pygame.draw.circle(screen, (255, 255, 255), (_), 1)

    for body in bodies:
        pygame.draw.circle(screen, (body["color"]), (body["x"], body["y"]), body["radius"])


    

    



    # Update the display
    pygame.display.flip() 
    clock.tick(fps_of_game)

pygame.quit()