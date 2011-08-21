import random
import pygame

# TODO: doesn't work for some reason
#from blobulous import SCREEN_W, SCREEN_H
SCREEN_W = 800
SCREEN_H = 600

POWERUP_SIZE = 12
POWERUP_COLOR = (0, 255, 0)

# TODO: should this just inherit from Enemy? They share a lotta code...
class Powerup(pygame.sprite.Sprite):

    # -- Attributes

    # Set speed vector
    change_x=0
    change_y=0

    # Whether this powerup is currently targeted by the player
    targeted = False
     
    # -- Methods

    # TODO: not sure if I have to set default values for x and y, but I want to
    # be able to just go Powerup(randomize=True) without passing in x and y
    # values, so default values seem necessary.
    def __init__(self, x=0, y=0, randomize=False):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
         
        # Set height, width
        self.image = pygame.Surface([POWERUP_SIZE, POWERUP_SIZE])
        self.image.fill((POWERUP_COLOR))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        
        if randomize == False:
            self.rect.topleft = [x, y]
        else:
            rand_x = random.randint(0, SCREEN_W - POWERUP_SIZE)
            rand_y = random.randint(0, SCREEN_H - POWERUP_SIZE)
            self.rect.topleft = [rand_x, rand_y]
     
    # Change the speed of the powerup
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
         
    # Find a new position for the powerup
    def update(self):
        self.rect.top += self.change_y
        self.rect.left += self.change_x
