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


class Cursor(pygame.sprite.Sprite):

    def __init__(self, *containers):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self, containers)

        # Load the image
        self.image = pygame.image.load("images/cursor.png").convert()
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [0, 0]
