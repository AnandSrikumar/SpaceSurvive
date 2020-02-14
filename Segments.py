import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class PlayerSegment(pygame.sprite.Sprite):

    def __init__(self, x, y, img, angle1=0, rotate=False, wid=80, hie=80):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.rotate(self.image, -90)
        self.image = pygame.transform.scale(self.image, (wid, hie))
        if rotate:
            self.image = pygame.transform.rotate(self.image, angle1)

        self.image.set_colorkey(WHITE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.width = self.image.get_width()
        self.height = self.image.get_height()


class Background(pygame.sprite.Sprite):
    def __init__(self, x, y, img, code='RGBX', wid=0, hie=0, s_w=0, s_h=0, frombuff=False):
        super().__init__()
        if frombuff:
            self.image = pygame.image.frombuffer(img, (wid, hie), code).convert_alpha()
        else:
            self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(self.image, (wid, hie))
        self.image.set_colorkey(WHITE)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]
        self.width = self.image.get_width()
        self.height = self.image.get_height()