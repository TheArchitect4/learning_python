import math
import pygame


Gravitational_constant = 10
bounciness = 0.99

class Body:
    
    def __init__(self, mass, radius, x, y, vx, vy,  color, fixed=False):
        self.mass = mass
        self.radius = radius
        self.x = x
        self.y = y 
        self.vx = vx
        self.vy = vy

        self.color = color
        self.fixed = fixed

        self.fx = 0.0
        self.fy = 0.0
    
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
    
        distance = math.hypot(dx, dy)
        if distance == 0:
            distance = 0.001
        return dx, dy, distance
    
    ### Calcu gravitational interaction with each pair of bodies, and add it to a resultant force --- store for calculation. combonation saves us here from counting and adding for forces for say mars - earch and earth - mars interaction. so as we go through the list, itll add each EM ES SUM (E=earch, S=Sun, M=Mars) forces and get a total resultant force for each body, from that we can then calculate the velocitry 
    def attract(self, other):
        
        dx, dy, distance = self.distance_to(other)
        dist_sq = dx*dx + dy*dy
        soft_srt = dist_sq + 1
        gravitational_force_over_distance = Gravitational_constant * self.mass * other.mass / ((dist_sq + 1) * distance)
        ### Fcosx=F_x
        ### fsinx=F_y
        self.fx += gravitational_force_over_distance * dx 
        self.fy += gravitational_force_over_distance * dy 
        ### Equal and opposite forces -=
        other.fx -= gravitational_force_over_distance * dx 
        other.fy -= gravitational_force_over_distance * dy 

    def colide(self, other):
        
        dx = other.x - self.x          # pre-check lives here
        dy = other.y - self.y
        min_dist = self.radius + other.radius
        if dx * dx + dy * dy > min_dist * min_dist:
            return
        dx, dy, distance = self.distance_to(other)
       

        norm_x = dx / distance
        norm_y = dy / distance
        
        
        ### Find the norm of the direction vector, 1/d (dx, dy) 
        ### this is a clap to provent the balls from merging, and we move them scaled by each of their masses, so the big one doesnt get tp'd by the small one
        overlap = (self.radius + other.radius) - distance + 0.001
        total_mass = self.mass + other.mass
        
        self.x += -norm_x * overlap * (other.mass / total_mass) 
        self.y+= -norm_y * overlap * (other.mass / total_mass) 

        
        other.x += norm_x * overlap * (self.mass / total_mass)
        other.y += norm_y * overlap * (self.mass / total_mass) 
        ### Relative velocity between bodies
        relative_v_x = other.vx - self.vx
        relative_v_y = other.vy - self.vy
        # Find speed along norm -- dot product
        velocity_along_norm = (norm_x * relative_v_x) + (norm_y * relative_v_y)




        if velocity_along_norm < 0:

            mass_factor = (1 / self.mass) + (1 / other.mass)

            impulse = -(1 + bounciness) * velocity_along_norm / mass_factor
                
            
            self.vx -= impulse * (1 / self.mass) * norm_x
            self.vy -= impulse * (1 / self.mass) * norm_y

            other.vx += impulse * (1 / other.mass) * norm_x
            other.vy += impulse * (1 / other.mass) * norm_y

    def reset_forces(self):
        self.fx = 0
        self.fy = 0

    def integration(self, dt, screen_width, screen_height):
        if self.fixed:
            return
        ### v=u+at a=f/m
        self.vx = self.vx + ((self.fx / self.mass) * dt)
        self.vy = self.vy + ((self.fy / self.mass) * dt)

        ### somehow stumbled onto the right method for this???  update velocity then position produces a stable orbit, but position then velocity gives me a spiral, learning more about why this happens --- semi-implicit Euler algorith 

        self.x = self.x + self.vx * dt
        self.y= self.y+ self.vy * dt
    

        if self.x - self.radius < 0 or self.x + self.radius > screen_width:
            self.x = max(self.radius, min(self.x, screen_width - self.radius))
            self.vx = -self.vx * 0.8
        
        if self.y - self.radius < 0 or self.y+ self.radius > screen_height:
            self.y= max(self.radius, min(self.y, screen_height - self.radius))
            self.vy = -self.vy * 0.8            

    def draw(self, screen):
        pygame.draw.circle(screen, (self.color), (int(self.x), int(self.y)), self.radius)
