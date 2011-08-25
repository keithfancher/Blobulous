import random
import pygame

from enemy import Enemy
from settings import *


POWERUP_SIZE = 25 # TODO: kill this, unnecessary


# Inherits from Enemy class. That doesn't quite make sense, conceptually. They
# should probably both inherit from a TargetableObject class or something, but
# this works for now.
class Powerup(Enemy):

    def __init__(self, x=0, y=0, dx=0, dy=0, randomize=False):
        # Call the parent's constructor (which calls Sprite's constructor...)
        Enemy.__init__(self, x, y, dx, dy, randomize)
         
        # Load the image
        self.image = pygame.image.load("images/powerup.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        # This can be pretty much anything larger than the size of the sprite
        # itself -- the collision rect for this image is already fine, but
        # we're comparing with circles so this needs *some* radius value.
        self.radius = 20
        
        if randomize == False:
            self.rect.topleft = [x, y]
            self.delta_x = dx
            self.delta_y = dy
        else:
            # Random initial position
            rand_x = random.randint(0, SCREEN_W - POWERUP_SIZE)
            rand_y = random.randint(0, SCREEN_H - POWERUP_SIZE)
            self.rect.topleft = [rand_x, rand_y]

            # Random initial speed and direction
            self.delta_x = random.randint(-5, 6)
            self.delta_y = random.randint(-5, 6)
     

# Spawns a single randomly positioned and randomly moving Powerup
# TODO: this should just be in the fucking constructor of Powerup
def spawn_powerup():
    # Directional constants... makes this shit a bit easier to read
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

    # At top of screen, bottom, left, or right
    spawn_location = random.randint(0, 3)

    if spawn_location == TOP:
        x_pos = random.randint(0, SCREEN_W - POWERUP_SIZE)
        y_pos = -POWERUP_SIZE
        dx = random.randint(-5, 5)
        dy = random.randint(1, 5) # gotta move down

    elif spawn_location == BOTTOM:
        x_pos = random.randint(0, SCREEN_W - POWERUP_SIZE)
        y_pos = SCREEN_H + POWERUP_SIZE
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 0) # gotta move up

    elif spawn_location == LEFT:
        x_pos = -POWERUP_SIZE
        y_pos = random.randint(0, SCREEN_H)
        dx = random.randint(1, 5) # gotta move right
        dy = random.randint(-5, 5)

    elif spawn_location == RIGHT:
        x_pos = SCREEN_W
        y_pos = random.randint(0, SCREEN_H - POWERUP_SIZE)
        dx = random.randint(-5, 0) # gotta move left
        dy = random.randint(-5, 5)

    return Powerup(x_pos, y_pos, dx, dy)
