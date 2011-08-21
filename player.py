import pygame

from powerup import Powerup

PLAYER_SIZE = 10
PLAYER_COLOR = (0, 0, 255)
TARGET_LINE_COLOR = (255, 0, 0)

class Player(pygame.sprite.Sprite):
 
    # -- Attributes

    # Set speed vector
    change_x = 0
    change_y = 0

    # all the enemies/powerups the player is targeting
    targeted = pygame.sprite.Group()

    # Max targets can have at once... this will increase w/ powerups
    max_targets = 3;
     
    # -- Methods

    def __init__(self, x, y):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
         
        # Set height, width
        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill((PLAYER_COLOR))
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
     
    # Change the speed of the player
    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y
         
    # Find a new position for the player
    def update(self):
        self.rect.top += self.change_y
        self.rect.left += self.change_x

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
                pygame.draw.line(surface, TARGET_LINE_COLOR,
                    self.rect.center, target.rect.center)

    def power_up(self):
        self.max_targets += 1
        print "Powered up! Targets: %d" % self.max_targets

    def power_down(self):
        # can never target fewer than ONE enemy/powerup
        if self.max_targets > 1:
            self.max_targets -= 1
