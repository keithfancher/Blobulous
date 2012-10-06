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
