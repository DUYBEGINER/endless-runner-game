import Variables
import pygame, os
from pygame.examples.cursors import image




class button():
    def __init__(self,x,y,scale):
        super().__init__()
        self.default_image = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/home/Default.png'))
        self.hover_image = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/home/Hover.png'))
        width = self.default_image.get_width()
        height = self.default_image.get_height()

        self.default_image = pygame.transform.scale(self.default_image, (int(width * scale), int(height * scale)))
        self.hover_image = pygame.transform.scale(self.hover_image, (int(width * scale), int(height * scale)))

        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.image = self.hover_image
        else:
            self.image = self.default_image

        Variables.SCREEN.blit(self.image,(self.rect.x, self.rect.y))