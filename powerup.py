import random
import pygame

from enemy import Enemy

# TODO: doesn't work for some reason
#from blobulous import SCREEN_W, SCREEN_H
SCREEN_W = 800
SCREEN_H = 600

POWERUP_SIZE = 12
POWERUP_COLOR = (0, 255, 0)


# Inherits from Enemy class. That doesn't quite make sense, conceptually. They
# should probably both inherit from a TargetableObject class or something, but
# this works for now.
class Powerup(Enemy):

    # TODO: not sure if I have to set default values for x and y, but I want to
    # be able to just go Powerup(randomize=True) without passing in x and y
    # values, so default values seem necessary.
    def __init__(self, x=0, y=0, dx=0, dy=0, randomize=False):

        # Call the parent's constructor (which calls Sprite's constructor...)
        Enemy.__init__(self, x, y, dx, dy, randomize)
         
        # Set height, width
        self.image = pygame.Surface([POWERUP_SIZE, POWERUP_SIZE])
        self.image.fill((POWERUP_COLOR))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        
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
     
def spawn_powerup():
    pass
