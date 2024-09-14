import pygame, sys, os
from pygame import *
import Variables
import Stone_fall
from Stone_fall import stones
from Boom import booms_effect
from pygame.sprite import Group
import update_high_score
Stone_broken = Group()
Boom_broken = Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed, mode):
        super().__init__()
        # Biến
        self.Animation_list = []
        self.action = 0
        self.index = 0
        self.jump = False
        self.in_air = True
        self.vel_y = 0  # Vận tốc
        self.alive = True
        self.mode = mode
        self.update_time = pygame.time.get_ticks()
        # Là người chơi 1 hay người chơi 2
        if x == 150:
            self.pl = 'player1'
        else: self.pl = 'player2'
        # Load all animation
        Animation_type = ['Idle', 'Run', 'Jump2']
        for animation in Animation_type:
            # Reset list temp
            Temp_list = []
            # Đếm xem có bao nhiêu file ảnh trong folder dùng làm animation
            num_of_frames = len(os.listdir(os.path.join(Variables.current_dir, f'Asset/character/{animation}')))
            for i in range(num_of_frames):
                img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/character/{animation}/{i}.png'))
                img = pygame.transform.scale(img, (int((img.get_width() * scale)), (img.get_height() * scale)))
                Temp_list.append(img)
            self.Animation_list.append(Temp_list)

        # Load ảnh frame hiện tại
        self.image = self.Animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Giảm kích thước rect bao quang player để xử lí va chạm chính xác hơn
        self.rect.width = int(self.rect.width * 0.6)
        # thêm thuộc tính width và height để sử dụng kiểm tra va chạm
        self.width = self.rect.width
        self.height = self.rect.height

        # Các biến dùng để di chuyển, biến đổi
        self.speed = speed
        self.flip = False  # Kiểm tra lật qua lại

    # Xử lí di chuyển nhân vật
    def move_and_jump(self, moving_left, moving_right):
        dx = 0
        dy = 0
        self.on_ground = False
        # Movement logic
        if moving_left:
            dx -= self.speed
            self.flip = True
        if moving_right:
            dx += self.speed
            self.flip = False

        # Jumping logic
        if self.jump and not self.in_air:
            self.vel_y = -8
            self.jump = False
            self.in_air = True

        # Gravity
        self.vel_y += Variables.GRAVITY
        dy += self.vel_y
        # Collision checking
        dx, dy = self.check_collision(dx, dy)

        # Kiểm tra va chạm với đất
        if self.rect.bottom + dy > Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT:
            dy = Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT - self.rect.bottom
            self.in_air = False

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, SCREEN):
        self.update_animation()
        # Xuất hình ảnh, chỉnh sửa diện tích hiển thị
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect, (6, 0, self.width + 5, self.height))
        # pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)


    def check_collision(self, dx, dy):
        """
        Kiểm tra va chạm với các đối tượng tường, đá
        """
        # Kiem tra va cham tuong
        # Mode 1 player
        if self.mode == 'mode1':
            if Variables.WALL_RECT1.colliderect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height):
                self.rect.left = Variables.WALL_RECT1.right
                dx = 0
            if Variables.WALL_RECT2.colliderect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height):
                self.rect.right = Variables.WALL_RECT2.left
                dx = 0
        else: # Mode 2 player
            if self.pl == 'player1':
                if Variables.WALL_RECT1_MODE2.colliderect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height):
                    self.rect.left = Variables.WALL_RECT1_MODE2.right
                    dx = 0
                if Variables.WALL_RECT2_MODE2.colliderect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height):
                    self.rect.right = Variables.WALL_RECT2_MODE2.left
                    dx = 0
            if self.pl == 'player2':
                if Variables.WALL_RECT3_MODE2.colliderect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height):
                    self.rect.left = Variables.WALL_RECT3_MODE2.right
                    dx = 0
                if Variables.WALL_RECT4_MODE2.colliderect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height):
                    self.rect.right = Variables.WALL_RECT4_MODE2.left
                    dx = 0 

        # Kiểm tra va chạm với stone
        for tile in stones:
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.in_air = True
                if self.vel_y < 0:
                    self.vel_y = tile.vel_y
                    dy = self.vel_y
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile.rect.top - self.rect.bottom

        #Kiểm tra có đứng trên đá không
        for tile in stones:
            if tile.rect.colliderect(self.rect.left, self.rect.bottom, self.width, 1):
                self.in_air = False
                self.on_ground = True

        #Tạo list đá đang rơi
        falling_stones = [stone for stone in stones if stone.rect.bottom > self.rect.top]

        #Kiểm tra bị đá đè
        for stone in falling_stones:
            if self.rect.colliderect(stone.rect.left, stone.rect.bottom, stone.rect.width, 1) and not self.in_air:
                if Variables.quantity_shield == 0:
                    self.alive = False
                else:
                    Variables.quantity_shield -= 1
                    #Kiểm tra va chạm với stone hay boom để chạy animetion tương ứng
                    if isinstance(stone,Stone_fall.Stone):
                        stone_broken= Stone_broken_effect(stone.rect.centerx, self.rect.centery-32)
                        Stone_broken.add(stone_broken)
                        Variables.check_collision_boom = False
                    else:
                        boom_broken = Boom_broken_effect(stone.rect.centerx, self.rect.centery - 32)
                        Boom_broken.add(boom_broken)
                        Variables.check_collision_boom = True
                    stone.kill()
                    dy = 0
                    break

        # Bị boom nổ
        for tile in booms_effect:
            if self.rect.colliderect(tile.rect.left, tile.rect.top, tile.rect.width, tile.rect.height):
                if Variables.quantity_shield == 0:
                    self.alive = False
                    print("over!")
                else:
                    Variables.quantity_shield -= 1
        #Kiểm tra player có đứng trên mặt đất không
        if not self.on_ground:
            self.in_air = True
        #Giảm giật
        if abs(dy) < 1:
            dy = 0
        return dx, dy

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
        if self.index >= len(self.Animation_list[self.action]) - 1:
            self.index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.update_time = pygame.time.get_ticks()
            self.index = 0

class Stone_broken_effect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.index = 0
        self.x = x
        self.y = y
        self.update_time = pygame.time.get_ticks()
        # Load animation
        for i in range(20):
            img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Map/animation_broken/{i}.png'))
            img = pygame.transform.scale(img, (32, 32))
            self.animation_list.append(img)
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
            self.kill()

class Boom_broken_effect(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = []
        self.index = 0
        self.x = x
        self.y = y
        self.update_time = pygame.time.get_ticks()
        # Load animation
        for i in range(16):
            img = pygame.image.load(os.path.join(Variables.current_dir, f'Asset/Map/boom_broken/{i}.png'))
            img = pygame.transform.scale(img, (32, 32))
            self.animation_list.append(img)
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
            self.kill()