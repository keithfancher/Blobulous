#!/usr/bin/env python

import sys
import random
import pygame

from player import Player
from enemy import Enemy, spawn_enemy
from powerup import Powerup, spawn_powerup
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen size
SCREEN_W = 800
SCREEN_H = 600

# Random constants for testing
NUM_ENEMIES = 8
NUM_POWERUPS = 3
FPS = 30

 
# PyGame init stuff
pygame.init()
screen = pygame.display.set_mode([SCREEN_W, SCREEN_H])
pygame.display.set_caption('Blobulous')
clock = pygame.time.Clock()
 
# Create the player object
player = Player(SCREEN_W / 2, SCREEN_H / 2)

# Does this really need its own Sprite Group?
player_group = pygame.sprite.RenderPlain((player))

# Start by spawning NUM_ENEMIES random enemies
enemies = pygame.sprite.RenderPlain()
for i in range(0, NUM_ENEMIES):
    enemies.add(spawn_enemy())

# Create NUM_POWERUPS random powerups
# These just live in the "enemies" group, makes things easier... they're all
# Sprite objects anyway, and they're basically just benign enemies
for i in range(0, NUM_POWERUPS):
    enemies.add(spawn_powerup())

# Mouse state... need to know if the button is held down or not, not just when
# it's pressed or released. Maybe PyGame has a better way to do this?
mouse_down = False
 
# Main event loop
while True:
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print "Shutting everything down..."
            sys.exit(0)
 
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

    # Have to check if we're over an enemy with the mouse every frame even when
    # there isn't a MOUSEMOTION event, 'cause the player could be holding down
    # the button and an enemy could move under the mouse.
    #
    # This seems pretty inefficient, there's probably a better way to do this.
    if mouse_down:
        mouse_position = pygame.mouse.get_pos()
        for enemy in enemies:
            if enemy.rect.collidepoint(mouse_position):
                player.target_enemy(enemy)

    # For now, there's a 1/20 chance a new enemy will spawn. Later I'll make
    # this based on timing, the level, the score, etc.
    # Is there a better way to check for 1/20? This works, I guess...
    if random.randint(0, 19) == 10:
        enemies.add(spawn_enemy())

    # And a 1/50 chance a new powerup will spawn...
    if random.randint(0, 49) == 20:
        enemies.add(spawn_powerup())
                 
    # This actually moves the player block based on the current speed
    player.update()

    # This calles the update() function on every Sprite in the group, magically!
    enemies.update()
     
    # -- Draw everything
    # Clear screen
    screen.fill(BLACK)

    # Draw target lines
    player.draw_target_lines(screen)
     
    # Draw player
    player_group.draw(screen)
    
    # Draw enemies
    enemies.draw(screen)

    # Flip screen
    pygame.display.flip()
     
    # Pause
    clock.tick(FPS)
