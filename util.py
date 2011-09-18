import sys
import pygame


def print_text(screen, text, size, color, **kwargs):
    """Writes text to a given surface using pygame.font, or fails with a
    warning if pygame.font isn't available. The **kwargs are passed to
    get_rect(), and can be used to easily position the text on the target
    surface."""
    if not pygame.font:
        print "Warning: fonts disabled. Install pygame.font!"
    else:
        font = pygame.font.Font('fonts/inconsolata.otf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**kwargs)
        screen.blit(text_surface, text_rect)


def shut_down(screen, message="Shutting everything down..."):
    """There's an annoying delay while Pygame shuts down -- this function gives
    the user some visual indication that things are closing down properly, and
    the game's not just hanging."""
    print message
    print_text(screen, message, 25, pygame.Color('red'),
               midbottom=screen.get_rect().midbottom)
    pygame.display.flip()
    sys.exit()
