import pygame, sys
from pygame import *
import os
from Variables import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,scale,speed):
        super().__init__()
        #Animation idle
        self.Animation_list = []
        self.action = 0
        self.index = 0
        self.jump = False
        self.in_air = True
        self.vel_y = 0  # Vận tốc
        self.update_time = pygame.time.get_ticks()

        #Load all animation
        Animation_type = ['Idle','Run','Jump']
        for animation in Animation_type:
            # Reset list temp
            Temp_list = []
            #Đếm xem có bao nhiêu file ảnh trong folder dùng làm animation
            num_of_frames = len(os.listdir(f'Asset/character/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'Asset/character/{animation}/{i}.png')
                img = pygame.transform.scale(img, (int((img.get_width() * scale)), (img.get_height() * scale)))
                Temp_list.append(img)
            self.Animation_list.append(Temp_list)

        self.image = self.Animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #Các biến dùng để di chuyển, biến đổi
        self.speed = speed
        self.flip = False       #Kiểm tra lật qua lại

    # Xử lí di chuyển nhân vật
    def moving(self,moving_left,moving_right):
        dx = 0
        dy = 0
        # Tăng giảm tọa độ x dựa theo moving-left hoặc moving-right
        if moving_left:
            dx -= self.speed
            self.flip = True
            # self.direction = -1
        if moving_right:
            dx += self.speed
            self.flip = False
            # self.direction = 1

        #Jump
        if self.jump == True and self.in_air==False:
            self.vel_y = -10
            self.jump = False
            self.in_air = True

        #Thêm trọng lực
        self.vel_y += GRAVITY

        dy += self.vel_y

        #Kiểm tra player có chạm đất chưa
        if self.rect.bottom + dy > WINDOW_HEIGHT-GROUND_HEIGHT:
            dy = WINDOW_HEIGHT - GROUND_HEIGHT - self.rect.bottom
            self.in_air = False

        #Update position
        self.rect.x += dx
        self.rect.y += dy
    def draw(self,SCREEN,moving_left,moving_right):
        self.moving(moving_left, moving_right)
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update_animation(self):
        # Tốc độ nhanh chậm của animation
        ANIMATION_COOLDOWN = 80
        # Cập nhật hình ảnh dựa trên frame hiện tại
        self.image = self.Animation_list[self.action][self.index]
        # Kiểm tra xem đủ thời gian để chuyển qua frame tiếp theo chưa
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        # Nếu index vượt qua số lượng animation hiện tại thì reset trở về 0
        if self.index >= len(self.Animation_list[self.action])-1:
                self.index = 0

    #
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.update_time = pygame.time.get_ticks()
            self.index = 0
