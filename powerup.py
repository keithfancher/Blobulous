import pygame

from enemy import Enemy


class Powerup(Enemy):
    """Inherits from Enemy class. That doesn't quite make sense, conceptually.
    They should probably both inherit from a TargetableObject class or
    something, but this works great for now. I'll likely change this if/when I
    implement powerdowns."""

    def __init__(self, x=0, y=0, dx=0, dy=0, randomize=False):
        # Call the parent's constructor (which calls Sprite's constructor...)
        Enemy.__init__(self, x, y, dx, dy, randomize)

        # Load the image
        self.image = pygame.image.load("images/powerup.png").convert()
        self.image.set_colorkey(pygame.Color('black'))
        self.rect = self.image.get_rect()

        # This can be pretty much anything larger than the size of the sprite
        # itself -- the collision rect for this image is already fine, but
        # we're comparing with circles so this needs *some* radius value.
        self.radius = 20

        if randomize:
            self.random_spawn()
        else:
            self.rect.center = (x, y)
            self.delta_x = dx
            self.delta_y = dy
