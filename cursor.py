import pygame


class Cursor(pygame.sprite.Sprite):

    def __init__(self, x=0, y=0):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self, self.containers)

        # Load the image
        self.image = pygame.image.load("images/cursor.png").convert()
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
