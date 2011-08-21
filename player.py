import pygame

from powerup import Powerup
from settings import *

PLAYER_SIZE = 20
PLAYER_COLOR = BLUE
TARGET_LINE_COLOR = RED

class Player(pygame.sprite.Sprite):
 
    # -- Attributes

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
    # How about this: Everythign you kill is worth 100 points singly, but once
    # the initial score is added up, it's multiplied by the number you've
    # targeted. That's a good start...
    score = 0
     
    # -- Methods

    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
         
        # Set height, width
#        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
#        self.image.fill((PLAYER_COLOR))
        self.image = pygame.image.load("images/player.png").convert()
        self.image.set_colorkey(BLACK)
 
        # Make our top-left corner the passed-in location.
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
