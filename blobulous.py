#!/usr/bin/env python

import random
import pygame

import settings as s
from player import Player
from enemy import Enemy
from powerup import Powerup
from cursor import Cursor
from explosion import Explosion
from util import print_text, shut_down


def should_spawn_enemy(score):
    """There's a (prob_range / 30) chance an enemy will spawn. prob_range
    starts at 1, and increases by 1 every time the score increases by 10,000.
    If the player manages to get to 30/30, an enemy will spawn every
    frame..."""
    prob_range = (score / 10000) + 1
    return random.randint(1, 30) in range(1, prob_range + 1)


def should_spawn_powerup():
    """For now there's a 1/175 chance per frame a powerup will spawn"""
    return random.randint(1, 175) == 42


def left_mouse_down():
    """Return True if left mouse button is being held down, False otherwise"""
    (left, middle, right) = pygame.mouse.get_pressed()
    return left


def draw_pause_screen(surface):
    """Draw pause screen to given surface"""
    print_text(surface, "PAUSED", 100, pygame.Color('red'),
               midbottom=surface.get_rect().center)
    print_text(surface, "ESC to exit, any other key to resume", 25,
               pygame.Color('darkgray'),
               centerx=surface.get_rect().centerx,
               centery=surface.get_rect().centery + 20)


def draw_intro_screen(surface):
    """Draw intro screen to given surface"""
    print_text(surface, "[BLOBULOUS]", 200, pygame.Color('red'),
               center=surface.get_rect().center)
    print_text(surface, "Press any key to begin, or ESC to exit", 25,
               pygame.Color('darkgray'),
               centerx=surface.get_rect().centerx,
               centery=surface.get_rect().centery + 120)


def draw_death_screen(surface, score):
    """Draw death screen to given surface"""
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


def main():
    """ My main() man!"""
    pygame.init()
    pygame.display.set_caption('Blobulous')
    screen = pygame.display.set_mode([s.SCREEN_W, s.SCREEN_H])
    clock = pygame.time.Clock()

    # Initialize sprite groups
    players = pygame.sprite.Group() # might be good for multiplayer?
    enemies = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    cursors = pygame.sprite.Group()
    all_sprites = pygame.sprite.RenderPlain()

    # Assign default groups to each sprite class
    Player.containers = all_sprites, players
    Enemy.containers = all_sprites, enemies
    Powerup.containers = all_sprites, enemies # give their own group?
    Explosion.containers = all_sprites, explosions
    Cursor.containers = all_sprites, cursors

    # Create the player object
    player = Player(s.SCREEN_W / 2, s.SCREEN_H / 2)

    # Create the mouse cursor
    cursor = Cursor()
    # Setting the cursor to invisible seems to alter the mouse sensitivity
    # quite a bit, which I *don't* want. FIXME
#    pygame.mouse.set_visible(False)

    # Spawn NUM_INIT_ENEMIES random enemies
    for i in xrange(s.NUM_INIT_ENEMIES):
        enemies.add(Enemy(randomize=True))

    # Spawn NUM_INIT_POWERUPS random powerups
    # These live in the "enemies" sprite group, since they're basically just a
    # special type of enemy.
    for i in xrange(s.NUM_INIT_POWERUPS):
        enemies.add(Powerup(randomize=True))

    # Start the game paused and on the intro screen. This is a lazy way to
    # handle game state, but it works.
    game_paused = True
    intro_screen = True

    # Main event loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shut_down(screen)

            if event.type == pygame.KEYDOWN:
                player.process_keypress(event.key)

                if event.key == pygame.K_ESCAPE:
                    if game_paused or player.is_dead():
                        shut_down(screen)
                    else:
                        game_paused = True
                        pygame.event.set_grab(False) # ungrab when paused
                        player.untarget_all() # untarget all when paused

                # When the game is paused, any non-ESC key will unpause
                else:
                    if game_paused:
                        if intro_screen:
                            intro_screen = False
                        game_paused = False
                        pygame.event.set_grab(True) # grab for less annoyance

            if event.type == pygame.KEYUP:
                player.process_keyrelease(event.key)

            # Update the cursor position
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.center = event.pos

            # When the mouse button is released, kill any targeted enemies
            if event.type == pygame.MOUSEBUTTONUP:
                # Button 1 is left mouse button
                if event.button == 1 and not (game_paused or player.is_dead()):
                    player.kill_targeted()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 3 is right button... nuke 'em all!
                if event.button == 3 and not (game_paused or player.is_dead()):
                    player.nuke(enemies)

        # Move the cursor... maybe only do this when we get mouse movement?
        # TODO: is getting this directly faster than polling like we do above?
#        cursor.rect.center = pygame.mouse.get_pos()

        #  Target the proper enemies. This seems pretty inefficient -- there's
        #  probably a better way to do this.
        if left_mouse_down() and not (game_paused or player.is_dead()):
            for enemy in enemies:
                if enemy.rect.collidepoint(pygame.mouse.get_pos()):
                    player.target_enemy(enemy)

        # Randomly spawn enemies and powerups.
        if should_spawn_enemy(player.score) and not game_paused:
            enemies.add(Enemy(randomize=True))
        if should_spawn_powerup() and not game_paused:
            enemies.add(Powerup(randomize=True))

        # Checks for collisions, destroys appropriate objects. Note use of
        # collide_circle -- a bit slower, but much more accurate for our
        # purposes.
        if not s.PLAYER_INVINCIBLE:
            if pygame.sprite.spritecollide(player, enemies, True,
                                           pygame.sprite.collide_circle):
                player.untarget_all()
                player.decrease_lives()
                if player.is_dead():
                    pygame.event.set_grab(False)

        screen.fill(pygame.Color('black'))
        if game_paused and not intro_screen:
            draw_pause_screen(screen)
        elif game_paused and intro_screen:
            draw_intro_screen(screen)
        elif player.is_dead():
            draw_death_screen(screen, player.score)
        else:
            # All the sprite groups
            all_sprites.update()
            player.draw_target_lines(screen)
            all_sprites.draw(screen) # Any way to control order of drawing?

            # Score, target meter, nuke indicator, number of lives
            player.draw_score(screen)
            player.draw_target_meter(screen)
            player.draw_nukes(screen)
            player.draw_num_lives(screen)

        # Draw FPS
        if s.SHOW_FPS:
            print_text(screen, "%.2f" % clock.get_fps(), 20,
                       pygame.Color('white'),
                       bottom=screen.get_rect().bottom - 8, left=10)

        # Flip & pause
        pygame.display.flip()
        clock.tick(s.FPS)


if __name__ == "__main__":
    main()
