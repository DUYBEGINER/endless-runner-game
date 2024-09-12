import pygame, os, random

from pygame.sprite import Group
from Stone_fall import stones

import Variables


GRAVITY_BOOM = 0.025

booms_effect = Group()
# Cài đặt thời gian chờ
ANIMATION_COOLDOWN = 360
pygame.mixer.init()
exploision_sfx =   pygame.mixer.Sound(os.path.join(Variables.current_dir, f'Asset/SFX/exploision.mp3'))
countdown_boom =   pygame.mixer.Sound(os.path.join(Variables.current_dir, f'Asset/SFX/countdown_boom.mp3'))
countdown_boom.set_volume(0.1)
exploision_sfx.set_volume(0.5)
# channel1 = pygame.mixer.Channel(1)  # Chọn kênh 1
# channel2 =  pygame.mixer.Channel(2)


class boom(pygame.sprite.Sprite):
    def __init__(self, scale):
        pygame.sprite.Sprite.__init__(self)
        self.scale = scale
        self.animation_list = []
        self.type = 'boom'
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.active = False
        # self.countdown_sound = countdown_boom
        # self.exploision_sound = exploision_sfx
        # Load image
        for i in range(1, 9):
            img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Boom/{i}.png'))
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            self.animation_list.append(img)
        self.image = self.animation_list[self.index]
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
            self.active = True
            self.vel_y = 0
            self.rect.bottom = Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT + 1
        else:
            self.in_air = True
        # Kiểm tra va chạm với stones
        self.check_collision_stones()
        self.update_animation()
        # Áp dụng Gravity
        if self.in_air:
            self.vel_y += GRAVITY_BOOM
            if self.vel_y > self.MAX_VEL:
                self.vel_y = self.MAX_VEL
        dy = self.vel_y
        self.rect.centery += dy
        self.check_to_delete()

    def check_collision_stones(self):
        for i in stones:
            if self != i:
                if (self.rect.centerx < i.rect.right and
                        self.rect.centerx > i.rect.left and
                        self.rect.bottom <= i.rect.top + 5 and
                        self.rect.bottom >= i.rect.top):
                    self.in_air = False
                    self.active = True
                    self.vel_y = 0
                    self.rect.bottom = i.rect.top + 1
                    break
                else:
                    self.in_air = True

    def update_animation(self):
        if self.active:
            countdown_boom.play()
            # Cập nhật frame ảnh hiện tại
            self.image = self.animation_list[self.index]
            #
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.index += 1
            if self.index >= len(self.animation_list):
                countdown_boom.stop()
                self.booom()
                exploision_sfx.play()



    def booom(self):
        list_tmp = []
        for stone in stones:
            if self != stone:
                if stone.rect.colliderect(self.rect.left - self.rect.width / 2, self.rect.top - self.rect.height / 2,
                                          self.rect.width * 2, self.rect.height * 2):
                    list_tmp.append(stone)
        for i in list_tmp:
            i.kill()
        list_tmp = []
        boom_effect = Boom_effect(self.rect.centerx, self.rect.centery)
        booms_effect.add(boom_effect)
        Variables.is_exploi = True
        self.kill()

    def check_to_delete(self):
        # reset list_to_delete
        self.list_to_delete = []
        for i in stones:
            if (i.rect.bottom >= Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT - 2):
                self.list_to_delete.append(i)
        if len(self.list_to_delete) == 8:
            # self.countdown_sound.stop()
            for i in self.list_to_delete:
                i.kill()




class Boom_effect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.index = 0
        self.x = x
        self.y = y
        self.update_time = pygame.time.get_ticks()
        # Load animation
        for i in range(1, 14):
            tmp_img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Boom/Boom_effect2/{i}.png'))
            self.animation_list.append(tmp_img)
        self.rect = self.animation_list[self.index].get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        ANIMATION_COOLDOWN_effect = 10
        # Cập nhật frame ảnh hiện tại
        self.image = self.animation_list[self.index]

        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN_effect:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.animation_list):
            Variables.is_exploi = False
            self.kill()