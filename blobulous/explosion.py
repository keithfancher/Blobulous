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


class Explosion(pygame.sprite.Sprite):

    def __init__(self, pos, *containers):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self, containers)

        self.images = []
        self.frame = 0
        self.frame_count = 0

        # Load images (7 frames)
        for i in xrange(7):
            filename = "images/explosion%d.png" % i
            self.images.append(pygame.image.load(filename).convert())
            self.images[i].set_colorkey((69, 78, 91))

        self.image = self.images[self.frame]
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        """Animate the explosion"""
        self.frame_count += 1

        # slow the explosion animation down a tad
        # TODO: make this less retarded, only render every other frame in a
        # better way...
        if self.frame_count > 1:
            self.frame_count = 0
            self.frame += 1
            if self.frame >= 7:
                self.kill()
            else:
                self.image = self.images[self.frame]
