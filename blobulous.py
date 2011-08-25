#!/usr/bin/env python

import sys
import random
import pygame

from player import Player
from enemy import Enemy, spawn_enemy
from powerup import Powerup, spawn_powerup
from settings import *
 

def main():
    # PyGame init stuff
    pygame.init()
    screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])
    pygame.display.set_caption('Blobulous')
    clock = pygame.time.Clock()

    # Testing font stuff
    if pygame.font:
        font = pygame.font.Font(None, 30)
    else:
        print "Warning: fonts disabled. Install pygame.font!"
     
    # Create the player object
    player = Player(SCREEN_W / 2, SCREEN_H / 2)
    # Doesn't need its own sprite group yet, but might be useful for multiplayer
    player_group = pygame.sprite.RenderPlain((player))

    # Spawn NUM_INIT_ENEMIES random enemies
    enemies = pygame.sprite.RenderPlain()
    for i in range(0, NUM_INIT_ENEMIES):
        enemies.add(spawn_enemy())

    # Spawn NUM_INIT_POWERUPS random powerups
    # These just live in the "enemies" group, makes things easier... they're
    # all Sprite objects anyway, and they're basically just benign enemies.
    for i in range(0, NUM_INIT_POWERUPS):
        enemies.add(spawn_powerup())

    # Mouse state... need to know if the button is held down or not, not just
    # when it's pressed or released. Maybe PyGame has a better way to do this?
    mouse_down = False

    # Grab input. Makes it easier to not lose focus when clicking around like a
    # madman in windowed mode. Also solves an input bug.
    pygame.event.set_grab(True)
     
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
                    print "Shutting everything down..."
                    sys.exit()
                     
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
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                player.kill_targeted()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True

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
        #
        # Is there a better way to check for 1/10? This works, I guess...
        if random.randint(0, 9) == 5:
            enemies.add(spawn_enemy())
            # Testing if enemies are actually destroyed once they're off-screen
            #print "Total enemies: %d" % len(enemies)

        # And a 1/100 chance a new powerup will spawn...
        if random.randint(0, 99) == 42:
            enemies.add(spawn_powerup())

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
                     
        # Moves the player based on the current speed/direction
        player.update()

        # Calls the update() function on every Sprite in the group, magically!
        enemies.update()
         
        # Draws everything
        screen.fill(pygame.Color('black'))
        player.draw_target_lines(screen)
        player_group.draw(screen)
        enemies.draw(screen)

        if pygame.font:
            # Draw the score to the screen
            # Recalculate the rect every time it's drawn, since the number can
            # continually grow and take up more space.
            # TODO: Really, only need to recalculate every time the score
            # increases.
            text = font.render(str(player.score), True, pygame.Color('white'))
            text_rect = text.get_rect()
            text_rect.bottom = screen.get_rect().bottom - 8
            text_rect.right = screen.get_rect().right - 10
            screen.blit(text, text_rect)

            # draw the FPS
            if SHOW_FPS:
                fps_text = font.render(str(clock.get_fps()), True, 
                                       pygame.Color('white'))
                fps_rect = fps_text.get_rect()
                fps_rect.bottom = screen.get_rect().bottom - 8
                fps_rect.left = 10
                screen.blit(fps_text, fps_rect)

        # Flip screen
        pygame.display.flip()
         
        # Pause
        clock.tick(FPS)


if __name__ == "__main__":
    main()
