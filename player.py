import pygame

from powerup import Powerup
from settings import *


class Player(pygame.sprite.Sprite):
 
    # Speed vector
    delta_x = 0
    delta_y = 0

    # All the enemies/powerups the player is targeting
    targeted = pygame.sprite.Group()

    max_targets = 2 # Max targets... increase w/ powerups
    extra_lives = 2 # Starting number
    score = 0
    apeshit_mode = False # Super powered up!!!
    radius = 10 # Used for circular collision detection
    images = [] # Images used for animation
     
    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Load images
        self.images.append(pygame.image.load("images/player_off.png").convert())
        self.images.append(pygame.image.load("images/player_on.png").convert())
        self.images[0].set_colorkey(pygame.Color('black'))
        self.images[1].set_colorkey(pygame.Color('black'))
         
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    # Change the speed of the player
    def changespeed(self, x, y):
        self.delta_x += x
        self.delta_y += y
         
    # Find a new position for the player
    def update(self):
        self.rect.top += self.delta_y
        self.rect.left += self.delta_x
        
        # For now, don't let player off-screen. Might change this up later.
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_W:
            self.rect.right = SCREEN_W
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_H:
            self.rect.bottom = SCREEN_H

        # if player is targeting an enemy, make him light up
        if self.targeted:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

    # Add an enemy to the targeted group
    def target_enemy(self, enemy):
        # don't target if we've reached our max
        if len(self.targeted) < self.max_targets:
            self.targeted.add(enemy)
            enemy.targeted = True

    # Remove enemy from the targeted group
    def untarget_enemy(self, enemy):
        self.targeted.remove(enemy)
        enemy.targeted = False

    # Remove all enemies from the targted group 
    def untarget_all(self):
        self.targeted.empty()

    # Kills all targeted enemies
    def kill_targeted(self):
        # 100 points for every enemy killed, then an additional multiplier for
        # killing mutliple enemies in one go.
        if self.apeshit_mode:
            # for now apeshit mode just doubles the score you'd get
            self.score += 100 * len(self.targeted) * len(self.targeted) * 2
        else:
            self.score += 100 * len(self.targeted) * len(self.targeted)
        for target in self.targeted:
            # Is this the best way to check for Powerup vs. Enemy?
            if isinstance(target, Powerup):
                self.power_up()
            else:
                # Eventually some score code should probably go here
                pass

            target.kill()
        
    # Draw the lines from self to targets
    def draw_target_lines(self, surface):
        # if there are sprites in the targeted group
        if(self.targeted):
            for target in self.targeted:
                pygame.draw.aaline(surface, pygame.Color('red'),
                                   self.rect.center, target.rect.center)

    def power_up(self):
        if self.max_targets < 10:
            self.max_targets += 1
            print "Powered up! Targets: %d" % self.max_targets
        else:
            # enter APESHIT MODE!!!
            self.apeshit_mode = True
            print "APESHIT MODE! SUPER SCORE BONUSES!"

    def power_down(self):
        # can never target fewer than ONE enemy/powerup
        if self.max_targets > 1:
            self.max_targets -= 1

    # Decrease lives and lower target # back to 2
    def decrease_lives(self):
        self.extra_lives -= 1
        self.max_targets = 2
        self.apeshit_mode = False # no more apeshit

    def is_dead(self):
        return self.extra_lives < 0
