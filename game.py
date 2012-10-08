# Copyright 2011, 2012 Keith Fancher
#
# This file is part of Blobulous.
#
# Blobulous is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Blobulous is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Blobulous.  If not, see <http://www.gnu.org/licenses/>.


import pygame
import random

import settings as s
from cursor import Cursor
from enemy import Enemy
from player import Player
from powerup import Powerup
from util import print_text, shut_down, left_mouse_down


class Game(object):

    def __init__(self):
        self.screen = pygame.display.set_mode([s.SCREEN_W, s.SCREEN_H])
        self.clock = pygame.time.Clock()

        # Create sprite groups
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.RenderPlain()

        # Create player and cursor
        self.player = Player(s.SCREEN_W / 2, s.SCREEN_H / 2, self.all_sprites)
        self.cursor = Cursor(self.all_sprites)

        # Start the game paused and on the intro screen. This is a lazy way to
        # handle game state, but it works.
        self.game_paused = True
        self.intro_screen = True

        # Setting the cursor to invisible seems to alter the mouse sensitivity
        # quite a bit, which I *don't* want. FIXME
        #pygame.mouse.set_visible(False)

    def spawn_enemies(self):
        """Spawn initial enemies in level."""
        for dummy in xrange(s.NUM_INIT_ENEMIES):
            self.enemies.add(Enemy(self.all_sprites, self.all_sprites, self.enemies))

    def spawn_powerups(self):
        """Spawn initial powerups in level."""
        for dummy in xrange(s.NUM_INIT_POWERUPS):
            self.enemies.add(Powerup(self.all_sprites, self.enemies))

    def should_spawn_enemy(self):
        """There's a (prob_range / 30) chance an enemy will spawn. prob_range
        starts at 1, and increases by 1 every time the score increases by
        10,000.  If the player manages to get to 30/30, an enemy will spawn
        every frame..."""
        prob_range = (self.player.score / 10000) + 1
        return random.randint(1, 30) in range(1, prob_range + 1)

    def should_spawn_powerup(self):
        """For now there's a 1/175 chance per frame a powerup will spawn."""
        return random.randint(1, 175) == 42

    def draw_pause_screen(self):
        """Draw pause screen."""
        print_text(self.screen, "PAUSED", 100, pygame.Color('red'),
                   midbottom=self.screen.get_rect().center)
        print_text(self.screen, "ESC to exit, any other key to resume", 25,
                   pygame.Color('darkgray'),
                   centerx=self.screen.get_rect().centerx,
                   centery=self.screen.get_rect().centery + 20)

    def draw_intro_screen(self):
        """Draw intro screen."""
        print_text(self.screen, "[BLOBULOUS]", 200, pygame.Color('red'),
                   center=self.screen.get_rect().center)
        print_text(self.screen, "Press any key to begin, or ESC to exit", 25,
                   pygame.Color('darkgray'),
                   centerx=self.screen.get_rect().centerx,
                   centery=self.screen.get_rect().centery + 120)

    def draw_death_screen(self):
        """Draw death screen."""
        print_text(self.screen, "YOU PIED.", 100, pygame.Color('red'),
                   midbottom=self.screen.get_rect().center)
        print_text(self.screen, "ESC to exit", 25,
                   pygame.Color('darkgray'),
                   centerx=self.screen.get_rect().centerx,
                   centery=self.screen.get_rect().centery + 20)
        print_text(self.screen, "Final score: %d" % self.player.score, 30,
                   pygame.Color('white'),
                   centerx=self.screen.get_rect().centerx,
                   centery=self.screen.get_rect().centery + 130)

    def process_keypress(self, key):
        """Process key presses."""
        self.player.process_keypress(key) # Player gets first whack at keys

        if key == pygame.K_ESCAPE:
            if self.game_paused or self.player.is_dead():
                shut_down(self.screen)
            else:
                self.game_paused = True
                pygame.event.set_grab(False) # ungrab when paused
                self.player.untarget_all() # untarget all when paused

        # When the game is paused, any non-ESC key will unpause
        else:
            if self.game_paused:
                if self.intro_screen:
                    self.intro_screen = False
                self.game_paused = False
                pygame.event.set_grab(True) # grab for less annoyance

    def process_event(self, event):
        """Process pygame events."""
        if event.type == pygame.QUIT:
            shut_down(self.screen)

        if event.type == pygame.KEYDOWN:
            self.process_keypress(event.key)

        if event.type == pygame.KEYUP:
            self.player.process_keyrelease(event.key)

        if event.type == pygame.MOUSEMOTION:
            # Update the cursor position
            self.cursor.rect.center = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            # When the mouse button 1 is released, kill any targeted enemies
            if event.button == 1 and not (self.game_paused or self.player.is_dead()):
                self.player.kill_targeted()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # 3 is right button... nuke 'em all!
            if event.button == 3 and not (self.game_paused or self.player.is_dead()):
                self.player.nuke(self.enemies)

    def update(self):
        """Update the game state. Called every frame."""
        # Target the proper enemies. This seems pretty inefficient -- there's
        # probably a better way to do this.
        if left_mouse_down() and not (self.game_paused or self.player.is_dead()):
            for enemy in self.enemies:
                if enemy.rect.collidepoint(pygame.mouse.get_pos()):
                    self.player.target_enemy(enemy)

        # Randomly spawn enemies and powerups.
        if self.should_spawn_enemy() and not self.game_paused:
            self.enemies.add(Enemy(self.all_sprites, self.all_sprites, self.enemies))
        if self.should_spawn_powerup() and not self.game_paused:
            self.enemies.add(Powerup(self.all_sprites, self.enemies))

        # Checks for collisions, destroys appropriate objects. Note use of
        # collide_circle -- a bit slower, but much more accurate for our
        # purposes.
        if not s.PLAYER_INVINCIBLE:
            if pygame.sprite.spritecollide(self.player, self.enemies, True,
                                           pygame.sprite.collide_circle):
                self.player.untarget_all()
                self.player.decrease_lives()
                if self.player.is_dead():
                    pygame.event.set_grab(False)

    def draw(self):
        """Draw everything!"""
        self.screen.fill(pygame.Color('black'))
        if self.game_paused and not self.intro_screen:
            self.draw_pause_screen()
        elif self.game_paused and self.intro_screen:
            self.draw_intro_screen()
        elif self.player.is_dead():
            self.draw_death_screen()
        else:
            # All the sprite groups
            self.all_sprites.update()
            self.player.draw_target_lines(self.screen)
            self.all_sprites.draw(self.screen) # Can I control draw order?

            # Score, target meter, nuke indicator, number of lives
            self.player.draw_score(self.screen)
            self.player.draw_target_meter(self.screen)
            self.player.draw_nukes(self.screen)
            self.player.draw_num_lives(self.screen)

        # Draw FPS
        if s.SHOW_FPS:
            print_text(self.screen, "%.2f" % self.clock.get_fps(), 20,
                       pygame.Color('white'),
                       bottom=self.screen.get_rect().bottom - 8, left=10)

        # Flip & pause
        pygame.display.flip()
        self.clock.tick(s.FPS)
