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


import sys
import pygame


def print_text(screen, text, size, color, **kwargs):
    """Writes text to a given surface using pygame.font, or fails with a
    warning if pygame.font isn't available. The **kwargs are passed to
    get_rect(), and can be used to easily position the text on the target
    surface."""
    if not pygame.font:
        sys.stderr.write("Warning: fonts disabled. Install pygame.font!\n")
    else:
        font = pygame.font.Font('fonts/inconsolata.otf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**kwargs)
        screen.blit(text_surface, text_rect)


def shut_down(screen, message="Shutting everything down..."):
    """There's an annoying delay while Pygame shuts down -- this function gives
    the user some visual indication that things are closing down properly, and
    the game's not just hanging."""
    sys.stderr.write(message + "\n")
    print_text(screen, message, 25, pygame.Color('red'),
               midbottom=screen.get_rect().midbottom)
    pygame.display.flip()
    sys.exit()


def left_mouse_down():
    """Return True if left mouse button is being held down, False otherwise."""
    (left, middle, right) = pygame.mouse.get_pressed()
    return left
