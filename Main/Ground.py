import pygame
import Variables

class Ground:

    if self.rect.bottom + dy > Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT:
        dy = Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT - self.rect.bottom
        self.in_air = False