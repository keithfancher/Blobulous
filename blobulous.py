#!/usr/bin/env python


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
