import random
import pygame

# TODO: doesn't work for some reason
#from blobulous import SCREEN_W, SCREEN_H
SCREEN_W = 800
SCREEN_H = 600

ENEMY_SIZE = 15
ENEMY_COLOR = (255, 255, 255)

class Enemy(pygame.sprite.Sprite):

    # -- Attributes

    # Set speed vector
    delta_x = 0
    delta_y = 0

    # Whether this enemy is currently targeted by the player
    targeted = False
     
    # -- Methods

    # TODO: not sure if I have to set default values for x and y, but I want to
    # be able to just go Enemy(randomize=True) without passing in x and y
    # values, so default values seem necessary.
    def __init__(self, x=0, y=0, dx=0, dy=0, randomize=False):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
         
        # Set height, width
        self.image = pygame.Surface([ENEMY_SIZE, ENEMY_SIZE])
        self.image.fill((ENEMY_COLOR))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        
        if randomize == False:
            self.rect.topleft = [x, y]
            self.delta_x = dx
            self.delta_y = dy
        else:
            # Random initial position
            rand_x = random.randint(0, SCREEN_W - ENEMY_SIZE)
            rand_y = random.randint(0, SCREEN_H - ENEMY_SIZE)
            self.rect.topleft = [rand_x, rand_y]

            # Random initial speed and direction
            self.delta_x = random.randint(-5, 6)
            self.delta_y = random.randint(-5, 6)
     
    # Change the speed of the enemy
    def changespeed(self, x, y):
        self.delta_x += x
        self.delta_y += y
         
    # Find a new position for the enemy
    def update(self):
        self.rect.top += self.delta_y
        self.rect.left += self.delta_x

    # Check this then kill any enemies that go off the screen.
    # Not sure if that's necessary, maybe PyGame automatically doesn't care
    # about off-screen Sprite objects? Seems prudent to kill 'em though.
    def is_offscreen(self):
        # TODO: can do this easily with rects?
        pass


def spawn_enemy():
    pass
