import random
import pygame

from explosion import Explosion
from settings import *


class Enemy(pygame.sprite.Sprite):

    # Set speed vector
    delta_x = 0
    delta_y = 0

    # Whether this enemy is currently targeted by the player
    targeted = False

    # Used by the circle collision detection. Allows a slightly smaller and
    # more accurate hit "box".
    radius = 21
     
    def __init__(self, x=0, y=0, dx=0, dy=0, randomize=False):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self, self.containers)
         
        # Load the image
        self.image = pygame.image.load("images/enemy.png").convert()
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        
        if randomize:
            self.random_spawn()
        else:
            self.rect.center = (x, y)
            self.delta_x = dx
            self.delta_y = dy

    # Find a new position for the enemy
    def update(self):
        self.rect.top += self.delta_y
        self.rect.left += self.delta_x
        # If we're more than 60 pixels off the screen, destroy the object
        self.kill_if_offscreen()

    # Override Sprite.kill() so enemies (and their descendent classes) will
    # explode instead of just disappearing
    def kill(self):
        # This is automatically added to the proper sprite group thanks to the
        # magic of Self.containers
        Explosion(self.rect.center)
        pygame.sprite.Sprite.kill(self)

    # Kill any enemies that go more than 60 pixels off the screen
    def kill_if_offscreen(self):
        if self.rect.left < -60 or self.rect.left > SCREEN_W + 60:
            self.kill()
        elif self.rect.top < -60 or self.rect.top > SCREEN_H + 60:
            self.kill()

    # Spawns somewhere off the screen with random direction and speed
    # TODO: Uses randint() incorrectly! Fix ranges for speeds.
    def random_spawn(self):
        # Directional constants... makes this shit a bit easier to read
        TOP = 0
        BOTTOM = 1
        LEFT = 2
        RIGHT = 3

        # At top of screen, bottom, left, or right
        spawn_location = random.randint(0, 3)

        if spawn_location == TOP:
            self.rect.left = random.randint(0, SCREEN_W - self.rect.width)
            self.rect.bottom = 0
            self.delta_x = random.randint(-5, 5)
            self.delta_y = random.randint(1, 5) # gotta move down

        elif spawn_location == BOTTOM:
            self.rect.left = random.randint(0, SCREEN_W - self.rect.width)
            self.rect.top = SCREEN_H
            self.delta_x = random.randint(-5, 5)
            self.delta_y = random.randint(-5, 0) # gotta move up

        elif spawn_location == LEFT:
            self.rect.right = 0
            self.rect.top = random.randint(0, SCREEN_H - self.rect.height)
            self.delta_x = random.randint(1, 5) # gotta move right
            self.delta_y = random.randint(-5, 5)

        elif spawn_location == RIGHT:
            self.rect.left = SCREEN_W
            self.rect.top = random.randint(0, SCREEN_H - self.rect.height)
            self.delta_x = random.randint(-5, 0) # gotta move left
            self.delta_y = random.randint(-5, 5)
