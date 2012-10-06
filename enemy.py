import random
import pygame

import settings as s
from explosion import Explosion


class Enemy(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0, dx=0, dy=0, randomize=False):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Set speed vector
        self.delta_x = 0
        self.delta_y = 0

        # Whether this enemy is currently targeted by the player
        self.targeted = False

        # Used by the circle collision detection. Allows a slightly smaller and
        # more accurate hit "box".
        self.radius = 21

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

    def update(self):
        """Update enemy position"""
        self.rect.top += self.delta_y
        self.rect.left += self.delta_x
        self.kill_if_offscreen() # Destroy object if offscreen

    def kill(self):
        """Override Sprite.kill() so enemies (and their descendent classes)
        will explode instead of just disappearing"""
        Explosion(self.rect.center) # added to proper Group automatically
        pygame.sprite.Sprite.kill(self)

    def kill_if_offscreen(self):
        """Kill any enemies that go more than 60 pixels off the screen"""
        if self.rect.left < -60 or self.rect.left > s.SCREEN_W + 60:
            self.kill()
        elif self.rect.top < -60 or self.rect.top > s.SCREEN_H + 60:
            self.kill()

    def random_spawn(self):
        """Spawns somewhere off the screen with random direction and speed"""

        # Directional constants... makes this shit a bit easier to read
        TOP = 0
        BOTTOM = 1
        LEFT = 2
        RIGHT = 3

        # At top of screen, bottom, left, or right
        spawn_location = random.randint(0, 3)

        if spawn_location == TOP:
            self.rect.left = random.randint(0, s.SCREEN_W - self.rect.width)
            self.rect.bottom = 0
            self.delta_x = random.randint(-5, 5)
            self.delta_y = random.randint(1, 5) # gotta move down

        elif spawn_location == BOTTOM:
            self.rect.left = random.randint(0, s.SCREEN_W - self.rect.width)
            self.rect.top = s.SCREEN_H
            self.delta_x = random.randint(-5, 5)
            self.delta_y = random.randint(-5, -1) # gotta move up

        elif spawn_location == LEFT:
            self.rect.right = 0
            self.rect.top = random.randint(0, s.SCREEN_H - self.rect.height)
            self.delta_x = random.randint(1, 5) # gotta move right
            self.delta_y = random.randint(-5, 5)

        elif spawn_location == RIGHT:
            self.rect.left = s.SCREEN_W
            self.rect.top = random.randint(0, s.SCREEN_H - self.rect.height)
            self.delta_x = random.randint(-5, -1) # gotta move left
            self.delta_y = random.randint(-5, 5)
