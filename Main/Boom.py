import pygame, os,  random
from Stone_fall import stones

import Variables
import Stone_fall
GRAVITY_BOOM = 0.025
class boom(pygame.sprite.Sprite):
    def __init__(self, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.animation_list = []
        self.type = 'boom'
        # Load image 
        for i in range(1, 9): 
            img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Boom/{1}.png'))
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            self.animation_list.append(img)
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()
        # Tạo vị trí ban đầu
        tmp = random.randint(1, 8)
        self.rect.center = (tmp * self.image.get_width() + self.image.get_width() / 2, -30)
        # Taọ các biến liên quan đến rơi
        self.in_air = True
        self.vel_y = 0
        self.MAX_VEL = 4
    def update(self):
        dy = 0
        # Kiểm tra đá có chạm mặt đất hay chưa
        if self.rect.bottom + dy > Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT:
            self.in_air = False
            self.vel_y = 0
            self.rect.bottom = Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT + 1
        else:
            self.in_air = True
        # Kiểm tra va chạm với stones
        self.check_collision_stones()
        # Áp dụng Gravity
        if self.in_air:
            self.vel_y += GRAVITY_BOOM
            if self.vel_y > self.MAX_VEL:
                self.vel_y = self.MAX_VEL
        dy = self.vel_y
        self.rect.centery += dy


    def check_collision_stones(self):
        for i in stones:
            if self != i:
                if (self.rect.centerx < i.rect.right and
                        self.rect.centerx > i.rect.left and
                        self.rect.bottom <= i.rect.top + 5 and
                        self.rect.bottom >= i.rect.top):
                    self.in_air = False
                    self.vel_y = 0
                    self.rect.bottom = i.rect.top + 1
                    break
                else:
                    self.in_air = True


