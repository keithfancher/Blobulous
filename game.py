import pygame
import random

import settings as s
from cursor import Cursor
from enemy import Enemy
from explosion import Explosion
from player import Player
from powerup import Powerup
from util import print_text, shut_down, left_mouse_down


class Game(object):

    def __init__(self):
        self.screen = pygame.display.set_mode([s.SCREEN_W, s.SCREEN_H])
        self.clock = pygame.time.Clock()

        self.init_sprite_groups()

        # Create player and cursor
        self.player = Player(s.SCREEN_W / 2, s.SCREEN_H / 2)
        self.cursor = Cursor()

        # Start the game paused and on the intro screen. This is a lazy way to
        # handle game state, but it works.
        self.game_paused = True
        self.intro_screen = True

        # Setting the cursor to invisible seems to alter the mouse sensitivity
        # quite a bit, which I *don't* want. FIXME
        #pygame.mouse.set_visible(False)

    def init_sprite_groups(self):
        """Initialize all the game's sprite groups and assign default groups as
        class variables to our different sprite classes."""
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.cursors = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.RenderPlain()

        # Assign default groups to each sprite class
        Player.containers = self.all_sprites, self.players
        Enemy.containers = self.all_sprites, self.enemies
        Powerup.containers = self.all_sprites, self.enemies # give their own group?
        Explosion.containers = self.all_sprites, self.explosions
        Cursor.containers = self.all_sprites, self.cursors

    def spawn_enemies(self):
        """Spawn initial enemies in level."""
        for i in xrange(s.NUM_INIT_ENEMIES):
            self.enemies.add(Enemy(randomize=True))

    def spawn_powerups(self):
        """Spawn initial powerups in level."""
        for i in xrange(s.NUM_INIT_POWERUPS):
            self.enemies.add(Powerup(randomize=True))

    def should_spawn_enemy(self, score):
        """There's a (prob_range / 30) chance an enemy will spawn. prob_range
        starts at 1, and increases by 1 every time the score increases by
        10,000.  If the player manages to get to 30/30, an enemy will spawn
        every frame..."""
        prob_range = (score / 10000) + 1
        return random.randint(1, 30) in range(1, prob_range + 1)

    def should_spawn_powerup(self):
        """For now there's a 1/175 chance per frame a powerup will spawn."""
        return random.randint(1, 175) == 42

    def draw_pause_screen(self, surface):
        """Draw pause screen to given surface."""
        print_text(surface, "PAUSED", 100, pygame.Color('red'),
                   midbottom=surface.get_rect().center)
        print_text(surface, "ESC to exit, any other key to resume", 25,
                   pygame.Color('darkgray'),
                   centerx=surface.get_rect().centerx,
                   centery=surface.get_rect().centery + 20)

    def draw_intro_screen(self, surface):
        """Draw intro screen to given surface."""
        print_text(surface, "[BLOBULOUS]", 200, pygame.Color('red'),
                   center=surface.get_rect().center)
        print_text(surface, "Press any key to begin, or ESC to exit", 25,
                   pygame.Color('darkgray'),
                   centerx=surface.get_rect().centerx,
                   centery=surface.get_rect().centery + 120)

    def draw_death_screen(self, surface, score):
        """Draw death screen to given surface."""
        print_text(surface, "YOU PIED.", 100, pygame.Color('red'),
                   midbottom=surface.get_rect().center)
        print_text(surface, "ESC to exit", 25,
                   pygame.Color('darkgray'),
                   centerx=surface.get_rect().centerx,
                   centery=surface.get_rect().centery + 20)
        print_text(surface, "Final score: %d" % score, 30,
                   pygame.Color('white'),
                   centerx=surface.get_rect().centerx,
                   centery=surface.get_rect().centery + 130)

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
        # Move the cursor... maybe only do this when we get mouse movement?
        # TODO: is getting this directly faster than polling like we do above?
#        cursor.rect.center = pygame.mouse.get_pos()

        # Target the proper enemies. This seems pretty inefficient -- there's
        # probably a better way to do this.
        if left_mouse_down() and not (self.game_paused or self.player.is_dead()):
            for enemy in self.enemies:
                if enemy.rect.collidepoint(pygame.mouse.get_pos()):
                    self.player.target_enemy(enemy)

        # Randomly spawn enemies and powerups.
        if self.should_spawn_enemy(self.player.score) and not self.game_paused:
            self.enemies.add(Enemy(randomize=True))
        if self.should_spawn_powerup() and not self.game_paused:
            self.enemies.add(Powerup(randomize=True))

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
            self.draw_pause_screen(self.screen)
        elif self.game_paused and self.intro_screen:
            self.draw_intro_screen(self.screen)
        elif self.player.is_dead():
            self.draw_death_screen(self.screen, self.player.score)
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
