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

from enemy import Enemy


class Powerup(Enemy):
    """Inherits from Enemy class. That doesn't quite make sense, conceptually.
    They should probably both inherit from a TargetableObject class or
    something, but this works great for now. I'll likely change this if/when I
    implement powerdowns."""

    def __init__(self, *containers):
        # Call the parent's constructor (which calls Sprite's constructor...)
        Enemy.__init__(self, containers)

        # Load the image
        self.image = pygame.image.load("images/powerup.png").convert()
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()

        # This can be pretty much anything larger than the size of the sprite
        # itself -- the collision rect for this image is already fine, but
        # we're comparing with circles so this needs *some* radius value.
        self.radius = 20

        self.random_spawn()
