import pygame

import settings as s
from powerup import Powerup
from util import print_text


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
    nukes = 0
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

        self.nuke_image = pygame.image.load("images/nuke.png").convert()
        self.nuke_image.set_colorkey(pygame.Color('black'))

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
        if self.rect.right >= s.SCREEN_W:
            self.rect.right = s.SCREEN_W
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= s.SCREEN_H:
            self.rect.bottom = s.SCREEN_H

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
            # Apeshit mode doubles the score you'd get
            self.score += 100 * len(self.targeted) * len(self.targeted) * 2
        else:
            self.score += 100 * len(self.targeted) * len(self.targeted)
        for target in self.targeted:
            if isinstance(target, Powerup):
                if self.apeshit_mode:
                    self.nukes = 1 # Only 1 nuke at a time
                else:
                    self.power_up()
            target.kill()

    # Nuke 'em all! Kills all enemies on screen.
    def nuke(self, enemy_group):
        if self.nukes:
            # No score bonuses when nuking. Also don't get any powerups.
            self.score += 100 * len(enemy_group)
            self.nukes -= 1
            for enemy in enemy_group:
                enemy.kill()

    # Draw nuke indicators (right now only one at a time)
    def draw_nukes(self, surface):
        if self.nukes:
            rect = self.nuke_image.get_rect(
                centerx=surface.get_rect().centerx + 125,
                centery=surface.get_rect().bottom - 22
            )
            surface.blit(self.nuke_image, rect)

    # Draw the lines from self to targets
    def draw_target_lines(self, surface):
        # if there are sprites in the targeted group
        if(self.targeted):
            for target in self.targeted:
                pygame.draw.aaline(surface, pygame.Color('red'),
                                   self.rect.center, target.rect.center)

    # Shows number of lives player has on given surface
    def draw_num_lives(self, surface):
        dest_rect = self.images[0].get_rect(
            right=surface.get_rect().right - 33,
            bottom=surface.get_rect().bottom - 40
        )
        surface.blit(self.images[0], dest_rect)
        if not self.is_dead():
            print_text(surface, "x%d" % self.extra_lives, 20,
                pygame.Color('white'),
                right=surface.get_rect().right - 10,
                bottom=surface.get_rect().bottom- 40
            )
        else:
            # Prevents showing negative lives
            print_text(surface, "x0", 20, pygame.Color('red'),
                       right=surface.get_rect().right - 10,
                       bottom=surface.get_rect().bottom - 40)

    # Draw a nifty target meter!
    def draw_target_meter(self, screen):
        meter_w = 200
        meter_h = 10
        targets = len(self.targeted)

        # change meter colors if player in apeshit mode
        if self.apeshit_mode:
            base_color = (78, 197, 219) # light blue
            bar_color = (255, 0, 255) # bright-ass pink-ish
        else:
            base_color = pygame.Color('yellow')
            bar_color = pygame.Color('red')

        surface = pygame.Surface((meter_w, meter_h))
        surface.fill(base_color)
        surface_rect = surface.get_rect(centerx=screen.get_rect().centerx,
                                        centery=screen.get_rect().bottom - 20)
        # inner!
        inner_w = (targets * meter_w) / self.max_targets
        inner_h = meter_h
        inner_surface = pygame.Surface((inner_w, inner_h))
        inner_surface.fill(bar_color)
        inner_rect = inner_surface.get_rect(topleft=surface_rect.topleft)

        # bliznit
        screen.blit(surface, surface_rect)
        screen.blit(inner_surface, inner_rect)

        # draw dividing lines
        segment_width = meter_w / self.max_targets
        line_x_pos = 0
        for i in xrange(self.max_targets - 1):
            line_x_pos += segment_width
            pygame.draw.line(screen, pygame.Color('black'),
                (surface_rect.left + line_x_pos, surface_rect.top),
                (surface_rect.left + line_x_pos, surface_rect.bottom)
            )

    # Draw the score on given surface
    def draw_score(self, surface):
        print_text(surface, str(self.score), 30, pygame.Color('white'),
                   bottom=surface.get_rect().bottom - 8,
                   right=surface.get_rect().right - 10)

    def power_up(self):
        if self.max_targets < 10:
            self.max_targets += 1
        else:
            # enter APESHIT MODE!!!
            self.apeshit_mode = True

    def power_down(self):
        # can never target fewer than ONE enemy/powerup
        if self.max_targets > 1:
            self.max_targets -= 1

    # Decrease lives and lower target # back to 2
    def decrease_lives(self):
        self.extra_lives -= 1
        self.max_targets = 2
        self.apeshit_mode = False # no more apeshit
        self.nukes = 0 # lose nukes when hit?

    def is_dead(self):
        return self.extra_lives < 0
