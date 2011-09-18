import pygame
import sys


# Writes text to a given surface using pygame.font, or fails with a warning if
# pygame.font isn't available.
def print_text(screen, text, size, color, **kwargs):
    if not pygame.font:
        print "Warning: fonts disabled. Install pygame.font!"
    else:
        font = pygame.font.Font('fonts/inconsolata.otf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**kwargs)
        screen.blit(text_surface, text_rect)


# There's an annoying delay while PyGame shuts down -- this function gives the
# user some visual indication that things are closing down properly, and it's
# not just hanging.
def shut_down(screen, message="Shutting everything down..."):
    print message
    print_text(screen, message, 25, pygame.Color('red'),
               midbottom=screen.get_rect().midbottom)
    pygame.display.flip()
    sys.exit()
