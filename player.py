import pygame

from powerup import Powerup
from settings import *


PLAYER_SIZE = 20 # TODO: kill this
TARGET_LINE_COLOR = pygame.Color('red')


class Player(pygame.sprite.Sprite):
 
    # Set speed vector
    change_x = 0
    change_y = 0

    # All the enemies/powerups the player is targeting
    targeted = pygame.sprite.Group()

    # Max targets can have at once... this will increase w/ powerups
    max_targets = 2

    # Beginning number of extra lives
    extra_lives = 3

    # Score!
    score = 0

    # This value is used for the circle collision detection
    radius = 10

    # The images used for animating the player
    images = []
     
    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Load images
        self.images.append(pygame.image.load("images/player_off.png").convert())
        self.images.append(pygame.image.load("images/player_on.png").convert())
        self.images[0].set_colorkey(pygame.Color('black'))
        self.images[1].set_colorkey(pygame.Color('black'))
         
        # Load the image
#        self.image = pygame.image.load("images/player.png").convert()
        self.image = self.images[0]
#        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
         
    # Find a new position for the player
    def update(self):
        self.rect.top += self.change_y
        self.rect.left += self.change_x
        
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
        self.score += 100 * len(self.targeted) * len(self.targeted)
        for target in self.targeted:
            # Is this the best way to check for Powerup vs. Enemy?
            if isinstance(target, Powerup):
                self.power_up()
            # Eventually some score code should probably go here
            else:
                pass
            target.kill()
        
    # Draw the lines from self to targets
    def draw_target_lines(self, surface):
        # if there are sprites in the targeted group
        if(self.targeted):
            for target in self.targeted:
                pygame.draw.aaline(surface, TARGET_LINE_COLOR,
                    self.rect.center, target.rect.center)

    def power_up(self):
        self.max_targets += 1
        print "Powered up! Targets: %d" % self.max_targets

    def power_down(self):
        # can never target fewer than ONE enemy/powerup
        if self.max_targets > 1:
            self.max_targets -= 1

    # Decrease lives and lower target # back to 2
    def decrease_lives(self):
        self.extra_lives -= 1
        self.max_targets = 2

    def is_dead(self):
        return self.extra_lives < 0
