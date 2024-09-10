import pygame, os,  random
from pygame.sprite import Group
from pygame.sprite import Sprite
import Stone_fall
from Stone_fall import stones
import Variables


Shield_Group = Group()
GRAVITY_SHIELD = 0.025

class shield(pygame.sprite.Sprite):
    def __init__(self, scale):
        Sprite.__init__(self)
        self.animation_list = []
        self.index = 0
        self.in_air =  True
        self.update_time = pygame.time.get_ticks()
        self.vel_y = 0


        for i in range(8):
            img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Item/Shield/{i}.png'))
            img = pygame.transform.scale(img, (int((img.get_width() * scale)), (img.get_height() * scale)))
            self.animation_list.append(img)

        self.image = self.animation_list[self.index]
        self.rect = self.image.get_rect()
        tmp = random.randint(1, 8)
        self.rect.center = (tmp * self.image.get_width() + self.image.get_width() / 2, -20)

    def update(self):
        dy = 0

        if self.rect.bottom + dy > Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT:
            self.in_air = False
            self.vel_y = 0
            self.rect.bottom = Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT + 1
        else:
            self.in_air = True

        if self.in_air:
            self.vel_y += GRAVITY_SHIELD
            dy += self.vel_y

        dy = self.check_collision_stone(dy)
        self.update_animation()

        self.rect.y += dy



    def check_collision_stone(self,dy):
        for stone in stones:
            if stone.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                self.in_air = False
                self.vel_y = 0
                dy = stone.rect.top - self.rect.bottom

        return dy


    def update_animation(self):
        # Tốc độ nhanh chậm của animation
        ANIMATION_COOLDOWN = 100
        # Cập nhật hình ảnh dựa trên frame hiện tại
        self.image = self.animation_list[self.index]
        # Kiểm tra xem đủ thời gian để chuyển qua frame tiếp theo chưa
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        # Nếu index vượt qua số lượng animation hiện tại thì reset trở về 0
        if self.index >= len(self.animation_list) - 1:
            self.index = 0

    def check_collision_player(self, player):
        if self.rect.colliderect(player):
            Variables.quantity_shield += 1
            self.kill()