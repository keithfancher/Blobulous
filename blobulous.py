#!/usr/bin/env python


import pygame

from game import Game


def main():
    """ My main() man!"""
    pygame.init()
    pygame.display.set_caption('Blobulous')

    game = Game()

    game.spawn_enemies()
    game.spawn_powerups()

    # main event loop
    while True:
        for event in pygame.event.get():
            game.process_event(event)

        game.update()
        game.draw()


if __name__ == '__main__':
    main()
