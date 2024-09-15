import Variables
import pygame, os
from pygame.examples.cursors import image


class button():
    def __init__(self, default_img, hover_img,x,y,scale):
        super().__init__()
        self.default_image = default_img
        self.hover_image = hover_img
        width = self.default_image.get_width()
        height = self.default_image.get_height()
        self.hover_first_time = 1
        self.default_image = pygame.transform.scale(self.default_image, (int(width * scale), int(height * scale)))
        self.hover_image = pygame.transform.scale(self.hover_image, (int(width * scale), int(height * scale)))

        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.hover_first_time:
                Variables.hover_button_sfx.play()
                self.hover_first_time = 0
            self.image = self.hover_image
        else:
            self.image = self.default_image
            self.hover_first_time = 1


        Variables.SCREEN.blit(self.image,(self.rect.x, self.rect.y))