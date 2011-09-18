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


# Based on the player's current score, determines the probability of an enemy
# spawning that frame, then based on that probability it returns a bool that
# says if one should spawn or not.
def should_spawn_enemy(score):
    # There's a (prob_range / 30) chance an enemy will spawn. prob_range starts
    # at 1, and increases by 1 every time the score increases by 10,000. If the
    # player manages to get to 30/30, an enemy will spawn every frame...
    prob_range = (score / 10000) + 1
    return random.randint(1, 30) in range(1, prob_range + 1)


# Show pause screen
def draw_pause_screen(surface):
    print_text(surface, "PAUSED", 100, pygame.Color('red'),
               midbottom=surface.get_rect().center)
    print_text(surface, "ESC to exit, any other key to resume", 25,
               pygame.Color('darkgray'),
               centerx=surface.get_rect().centerx,
               centery=surface.get_rect().centery + 20)


# Show intro screen
def draw_intro_screen(surface):
    print_text(surface, "[BLOBULOUS]", 200, pygame.Color('red'),
               center=surface.get_rect().center)
    print_text(surface, "Press any key to begin, or ESC to exit", 25,
               pygame.Color('darkgray'),
               centerx=surface.get_rect().centerx,
               centery=surface.get_rect().centery + 120)


# Show death screen
def draw_death_screen(surface, score):
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


# My main() man
def main():

    # PyGame init stuff
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
    # quite a bit, which I *don't* want.
#    pygame.mouse.set_visible(False)

    # Spawn NUM_INIT_ENEMIES random enemies
    for i in xrange(s.NUM_INIT_ENEMIES):
        enemies.add(Enemy(randomize=True))

    # Spawn NUM_INIT_POWERUPS random powerups
    # These just live in the "enemies" group, makes things easier... they're
    # all Sprite objects anyway, and they're basically just benign enemies.
    for i in xrange(s.NUM_INIT_POWERUPS):
        enemies.add(Powerup(randomize=True))

    # Mouse state... need to know if the button is held down or not, not just
    # when it's pressed or released. Maybe PyGame has a better way to do this?
    mouse_down = False

    # Start the game paused and on the intro screen. This is a lazy way to
    # handle game state, but it works.
    game_paused = True
    intro_screen = True

    # Main event loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shut_down(screen)

            # Set the speed based on the key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-3, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(3, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, -3)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, 3)

                if event.key == pygame.K_ESCAPE:
                    if game_paused or player.is_dead():
                        shut_down(screen)
                    else:
                        game_paused = True
                        pygame.event.set_grab(False) # ungrab when paused
                        player.untarget_all() # untarget all when paused
                        mouse_down = False # even if the mouse is actually down

                # When the game is paused, any non-ESC key will unpause
                else:
                    if game_paused:
                        if intro_screen:
                            intro_screen = False
                        game_paused = False
                        pygame.event.set_grab(True) # grab for less annoyance

            # Reset speed when key goes up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(3, 0)
                if event.key == pygame.K_RIGHT:
                    player.changespeed(-3, 0)
                if event.key == pygame.K_UP:
                    player.changespeed(0, 3)
                if event.key == pygame.K_DOWN:
                    player.changespeed(0, -3)

            # Update the cursor position
            if event.type == pygame.MOUSEMOTION:
                cursor.rect.center = event.pos

            # When the mouse button is released, kill any targeted enemies
            if event.type == pygame.MOUSEBUTTONUP:
                # Button 1 is left mouse button
                if event.button == 1 and not (game_paused or player.is_dead()):
                    mouse_down = False
                    player.kill_targeted()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not (game_paused or player.is_dead()):
                    mouse_down = True

                # Button 3 is right... nuke 'em!
                if event.button == 3 and not (game_paused or player.is_dead()):
                    player.nuke(enemies)

        # Move the cursor... maybe only do this when we get mouse movement?
#        cursor.rect.center = pygame.mouse.get_pos()

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

        # Randomly spawn enemies. The frequency of enemies spawning depends on
        # the score.
        if should_spawn_enemy(player.score) and not game_paused:
            enemies.add(Enemy(randomize=True))

        # And a 1/175 chance a new powerup will spawn...
        if random.randint(1, 175) == 42 and not game_paused:
            enemies.add(Powerup(randomize=True))

        # If a player has collided with anything at all.
        # Note that colliding with a Powerup will also kill the player. He's
        # gotta SHOOT the powerup if he wants it.
        if not s.PLAYER_INVINCIBLE:
            if pygame.sprite.spritecollideany(player, enemies):

                # This actually does the work of checking if the player should
                # die, and destroying any objects they've collided with. This
                # function is a bit slow, so only call it when we already KNOW
                # there's been a collision, instead of every frame. Note use of
                # collide_circle -- a bit slower, but much more accurate for
                # our purposes.
                if pygame.sprite.spritecollide(player, enemies, True,
                                               pygame.sprite.collide_circle):
                    player.untarget_all()
                    player.decrease_lives()
                    if player.is_dead():
                        pygame.event.set_grab(False)
                        mouse_down = False
                        print "That was your last life! You're dead."
                        print "Final score: %d" % player.score

        # Clear screen
        screen.fill(pygame.Color('black'))

        # Game is paused
        if game_paused and not intro_screen:
            draw_pause_screen(screen)

        # Intro screen
        elif game_paused and intro_screen:
            draw_intro_screen(screen)

        # The player is dead
        elif player.is_dead():
            draw_death_screen(screen, player.score)

        # Otherwise update/draw everything normally
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

        # Draw the FPS
        if s.SHOW_FPS:
            print_text(screen, "%.2f" % clock.get_fps(), 20,
                       pygame.Color('white'),
                       bottom=screen.get_rect().bottom - 8, left=10)

        # Flip screen
        pygame.display.flip()

        # Pause
        clock.tick(s.FPS)


if __name__ == "__main__":
    main()
