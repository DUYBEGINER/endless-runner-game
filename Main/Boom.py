import pygame, os, random, json

from pygame.sprite import Group
from Stone_fall import stones

import Variables
SETTINGS_FILE = 'settings.json'  # Tên tệp lưu trữ cài đặt
GRAVITY_BOOM = 0.025

booms_effect = Group()
# Cài đặt thời gian chờ
ANIMATION_COOLDOWN = 360
pygame.mixer.init()


# channel1 = pygame.mixer.Channel(1)  # Chọn kênh 1
# channel2 =  pygame.mixer.Channel(2)


class boom(pygame.sprite.Sprite):
    def __init__(self, difficulty):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.type = 'boom'
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        self.active = False
        if difficulty == 'Easy':
            self.dfc = 1.0
        elif difficulty == 'Normal':
            self.dfc = 1.25
        elif difficulty == 'Hard':
            self.dfc = 1.5
        elif difficulty == 'Hardest':
            self.dfc = 1.75
        if difficulty == "Hardest":
            self.scale = 3
        else:
            self.scale = 2
        # self.countdown_sound = countdown_boom
        # self.exploision_sound = exploision_sfx
        # Load image
        for i in range(1, 9):
            img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Boom/{i}.png'))
            img = pygame.transform.scale(img, (img.get_width() * 2, img.get_height() * 2))
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
            self.vel_y += GRAVITY_BOOM * self.dfc
            if self.vel_y > self.MAX_VEL * self.dfc:
                self.vel_y = self.MAX_VEL * self.dfc
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
            Variables.countdown_boom.play()
            # Cập nhật frame ảnh hiện tại
            self.image = self.animation_list[self.index]
            #
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.index += 1
            if self.index >= len(self.animation_list):
                Variables.countdown_boom.stop()
                self.booom()
                Variables.exploision_sfx.play()



    def booom(self):
        list_tmp = []
        for stone in stones:
            if self != stone:
                if stone.rect.colliderect(self.rect.left - self.rect.width / 2, self.rect.top - self.rect.height / 2,
                                          self.rect.width * self.scale, self.rect.height * self.scale):
                    list_tmp.append(stone)
        for i in list_tmp:
            i.kill()
        list_tmp = []
        boom_effect = Boom_effect(self.rect.centerx, self.rect.centery, Variables.list_rate[4])
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
    def __init__(self, x, y, difficulty):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.index = 0
        self.x = x
        self.y = y
        self.boom_broken_shield = 5
        self.update_time = pygame.time.get_ticks()
        if difficulty == "Hardest":
            self.scale = 1.25
        else:
            self.scale = 1
        # Load animation
        for i in range(1, 14):
            tmp_img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Boom/Boom_effect2/{i}.png'))
            tmp_img = pygame.transform.scale(tmp_img, (tmp_img.get_width() * self.scale, tmp_img.get_height() * self.scale))
            self.animation_list.append(tmp_img)
        self.rect = self.animation_list[self.index].get_rect()
        self.rect.center = (self.x, self.y)

    def update(self,player_alive):
        if player_alive:
            ANIMATION_COOLDOWN_effect = 10
            # Cập nhật frame ảnh hiện tại
            self.image = self.animation_list[self.index]

            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN_effect:
                self.update_time = pygame.time.get_ticks()
                self.index += 1
            if self.index >= len(self.animation_list):
                Variables.is_exploi = False
                self.kill()
        else:
            self.image = self.animation_list[7] #Để ảnh khi nhân vật chết thì hiện frame nổ to nhất để che nhân vật, trông thật hơn