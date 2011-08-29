#!/usr/bin/env python


import sys
import random
import pygame

from player import Player
from enemy import Enemy
from powerup import Powerup
from cursor import Cursor
from explosion import Explosion
from settings import *


# Write text to a given surface using pygame.font, or fails with a warning if
# pygame.font isn't available.
def print_text(screen, text, size, color, **kwargs):
    if not pygame.font:
        print "Warning: fonts disabled. Install pygame.font!"
    else:
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**kwargs)
        screen.blit(text_surface, text_rect)


# Draw a nifty target meter!
def draw_target_meter(screen, targets, max_targets):
    meter_w = 200
    meter_h = 10

    surface = pygame.Surface((meter_w, meter_h))
    surface.fill(pygame.Color('yellow'))
    surface_rect = surface.get_rect(centerx=screen.get_rect().centerx,
                                    centery=screen.get_rect().bottom - 20)
    # inner!
    inner_w = (targets * meter_w) / max_targets
    inner_h = meter_h
    inner_surface = pygame.Surface((inner_w, inner_h))
    inner_surface.fill(pygame.Color('red'))
    inner_rect = inner_surface.get_rect(topleft=surface_rect.topleft)
    
    # bliznit
    screen.blit(surface, surface_rect)
    screen.blit(inner_surface, inner_rect)

    # draw dividing lines
    segment_width = meter_w / max_targets
    line_x_pos = 0
    for i in xrange(max_targets - 1):
        line_x_pos += segment_width
        pygame.draw.line(screen, pygame.Color('black'),
                         (surface_rect.left + line_x_pos, surface_rect.top),
                         (surface_rect.left + line_x_pos, surface_rect.bottom))
 

# My main() man
def main():

    # PyGame init stuff
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])
    pygame.display.set_caption('Blobulous')
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
    player = Player(SCREEN_W / 2, SCREEN_H / 2)

    # Create the mouse cursor
    cursor = Cursor()
    # Setting the cursor to invisible seems to alter the mouse sensitivity
    # quite a bit, which I *don't* want.
#    pygame.mouse.set_visible(False)

    # Spawn NUM_INIT_ENEMIES random enemies
    for i in xrange(NUM_INIT_ENEMIES):
        enemies.add(Enemy(randomize=True))

    # Spawn NUM_INIT_POWERUPS random powerups
    # These just live in the "enemies" group, makes things easier... they're
    # all Sprite objects anyway, and they're basically just benign enemies.
    for i in xrange(NUM_INIT_POWERUPS):
        enemies.add(Powerup(randomize=True))

    # Mouse state... need to know if the button is held down or not, not just
    # when it's pressed or released. Maybe PyGame has a better way to do this?
    mouse_down = False

    # Grab input. Makes it easier to not lose focus when clicking around like a
    # madman in windowed mode. Also solves an input bug.
    pygame.event.set_grab(True)

    game_paused = False
     
    # Main event loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print "Shutting everything down..."
                sys.exit()
     
            # TODO: non-shitty keyboard controls... and joystick?
            # Set the speed based on the key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-3,0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(3,0)
                if event.key == pygame.K_UP:
                    player.changespeed(0,-3)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0,3)

                if event.key == pygame.K_ESCAPE:
                    if game_paused:
                        print "Shutting everything down..."
                        sys.exit()
                    else:
                        game_paused = True
                        pygame.event.set_grab(False) # ungrab when paused
                        player.untarget_all() # untarget all when paused
                        mouse_down = False # even if the mouse is actually down

                # When the game is paused, any non-ESC key will unpause
                else:
                    if game_paused:
                        game_paused = False
                        pygame.event.set_grab(True)
                     
            # Reset speed when key goes up      
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(3,0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-3,0)
                if event.key == pygame.K_UP:
                    player.changespeed(0,3)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0,-3)

            # Might do something with this later, but not now...
            if event.type == pygame.MOUSEMOTION:
                pass

            # When the mouse button is released, kill any targeted enemies
            # TODO: only left button
            if event.type == pygame.MOUSEBUTTONUP and not game_paused:
                mouse_down = False
                player.kill_targeted()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_paused:
                mouse_down = True

        # Move the cursor... maybe only do this when we get mouse movement?
        cursor.rect.center = pygame.mouse.get_pos()

        # Have to check if we're over an enemy with the mouse every frame even
        # when there isn't a MOUSEMOTION event, 'cause the player could be
        # holding down the button and an enemy could move under the mouse.
        #
        # This seems pretty inefficient, there's probably a better way to do
        # this.
        if mouse_down:
            mouse_position = pygame.mouse.get_pos()
            for enemy in enemies:
                if enemy.rect.collidepoint(mouse_position):
                    player.target_enemy(enemy)

        # For now, there's a 1/10 chance a new enemy will spawn. Later I'll
        # make this based on timing, the level, the score, etc.
        if random.randint(1, 10) == 5 and not game_paused:
            enemies.add(Enemy(randomize=True))

        # And a 1/175 chance a new powerup will spawn...
        if random.randint(1, 175) == 42 and not game_paused:
            enemies.add(Powerup(randomize=True))

        # If a player has collided with anything at all.
        # Note that colliding with a Powerup will also kill the player. He's
        # gotta SHOOT the powerup if he wants it.
        if not PLAYER_INVINCIBLE:
            if pygame.sprite.spritecollideany(player, enemies):

                # This actually does the work of checking if the player should
                # die, and destroying any objects they've collided with. This
                # function is a bit slow, so only call it when we already KNOW
                # there's been a collision, instead of every frame. Note use of
                # collide_circle -- a bit slower, but much more accurate for
                # our purposes.
                if pygame.sprite.spritecollide(player, enemies, True, 
                                               pygame.sprite.collide_circle):
                    player.decrease_lives()
                    if player.is_dead():
                        print "That was your last life! You're dead."
                        print "Final score: %d" % player.score
                        print "Shutting everything down..."
                        sys.exit()
                    else:
                        print "You lost a life. Remaining: %d" % player.extra_lives
                     
        # Update and draw all sprite groups
        screen.fill(pygame.Color('black'))
        if not game_paused:
            all_sprites.update()
            player.draw_target_lines(screen)
            all_sprites.draw(screen) # any way to control order of drawing?
        else:
            print_text(screen, "PAUSED", 50, pygame.Color('red'), 
                       midbottom=screen.get_rect().center)
            print_text(screen, "ESC to exit, any other key to resume", 25,
                       pygame.Color('darkgray'), 
                       centerx=screen.get_rect().centerx,
                       centery=screen.get_rect().centery + 20)

        # Draw the score
        print_text(screen, str(player.score), 30, pygame.Color('white'),
                   bottom=screen.get_rect().bottom - 8,
                   right=screen.get_rect().right - 10)

        # Draw the FPS
        if SHOW_FPS:
            print_text(screen, "%.2f" % clock.get_fps(), 30, 
                       pygame.Color('white'),
                       bottom=screen.get_rect().bottom - 8, left=10)

        # Draw the target meter
        draw_target_meter(screen, len(player.targeted), player.max_targets)

        # Flip screen
        pygame.display.flip()
         
        # Pause
        clock.tick(FPS)


if __name__ == "__main__":
    main()
