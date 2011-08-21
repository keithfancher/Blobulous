import random
import pygame

from settings import *

ENEMY_SIZE = 15
ENEMY_COLOR = WHITE

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
            # TODO: just realized this could be zero... and it would stay still
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
        # If we're more than 30 pixels off the screen, destroy the object
        self.kill_if_offscreen()

    # Kill any enemies that go more than 30 pixels off the screen
    def kill_if_offscreen(self):
        if self.rect.left < -30 or self.rect.left > SCREEN_W + 30:
            self.kill()
        elif self.rect.top < -30 or self.rect.top > SCREEN_H + 30:
            self.kill()


# Spawns a single randomly positioned and randomly moving Enemy
# TODO: this should just be in the fucking constructor of Enemy
def spawn_enemy():
    # Directional constants... makes this shit a bit easier to read
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

    # At top of screen, bottom, left, or right
    spawn_location = random.randint(0, 3)

    if spawn_location == TOP:
        x_pos = random.randint(0, SCREEN_W - ENEMY_SIZE)
        y_pos = -ENEMY_SIZE
        dx = random.randint(-5, 5)
        dy = random.randint(1, 5) # gotta move down

    elif spawn_location == BOTTOM:
        x_pos = random.randint(0, SCREEN_W - ENEMY_SIZE)
        y_pos = SCREEN_H + ENEMY_SIZE
        dx = random.randint(-5, 5)
        dy = random.randint(-5, 0) # gotta move up

    elif spawn_location == LEFT:
        x_pos = -ENEMY_SIZE
        y_pos = random.randint(0, SCREEN_H)
        dx = random.randint(1, 5) # gotta move right
        dy = random.randint(-5, 5)

    elif spawn_location == RIGHT:
        x_pos = SCREEN_W
        y_pos = random.randint(0, SCREEN_H - ENEMY_SIZE)
        dx = random.randint(-5, 0) # gotta move left
        dy = random.randint(-5, 5)

    return Enemy(x_pos, y_pos, dx, dy)
