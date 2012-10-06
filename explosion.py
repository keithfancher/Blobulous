import pygame


class Explosion(pygame.sprite.Sprite):

    def __init__(self, pos):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self, self.containers)

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
