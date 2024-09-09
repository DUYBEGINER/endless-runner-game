import pygame, sys, os
from pygame import *
import Variables
import Stone_fall
from Stone_fall import stones


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        super().__init__()
        # Biến
        self.Animation_list = []
        self.action = 0
        self.index = 0
        self.jump = False
        self.in_air = True
        self.vel_y = 0  # Vận tốc
        self.update_time = pygame.time.get_ticks()

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
    def Moving(self, moving_left, moving_right):
        dx = 0
        dy = 0
        # Tăng giảm tọa độ x dựa theo moving-left hoặc moving-right
        if moving_left:
            dx -= self.speed
            self.flip = True
        if moving_right:
            dx += self.speed
            self.flip = False

        # Sử dụng hàm kiểm tra va chạm
        dx, dy = self.check_collision(dx, dy)
        self.rect.x += dx
        self.rect.y += dy

    #### JUMP  #####
    def Jump(self):
        dx = 0
        dy = 0
        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -10
            self.jump = False
            self.in_air = True
        # Thêm trọng lực
        self.vel_y += Variables.GRAVITY
        dy += self.vel_y
        # Sử dụng hàm kiểm tra va chạm
        dx, dy = self.check_collision(dx, dy)
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, SCREEN):
        # Xuất hình ảnh, chỉnh sửa diện tích hiển thị
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect, (6, 0, self.width + 5, self.height))
        pygame.draw.rect(SCREEN, (255, 0, 0), self.rect, 2)

    def check_collision(self, dx, dy):
        """
        Kiểm tra va chạm với các đối tượng tường, đá
        """
        # Kiem tra va cham tuong
        if Variables.WALL_RECT1.colliderect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height):
            self.rect.left = Variables.WALL_RECT1.right
            dx = 0
        if Variables.WALL_RECT2.colliderect(self.rect.left + dx, self.rect.top, self.rect.width, self.rect.height):
            self.rect.right = Variables.WALL_RECT2.left
            dx = 0

        # Kiểm tra va chạm với stone
        for tile in stones:
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        self.vel_y = tile.vel_y
                        dy = self.vel_y
                    elif self.vel_y >= 0:
                        self.vel_y = 0
                        dy = tile.rect.top - self.rect.bottom

        for tile in stones:
            if tile.rect.colliderect(self.rect.left, self.rect.bottom, self.width, 1):
                self.in_air = False

        falling_stones = [stone for stone in stones if stone.rect.bottom > self.rect.top]
        for stone in falling_stones:
            if self.rect.colliderect(stone.rect) and not self.in_air:
                Variables.RUNNING = False

        # Kiểm tra va chạm với đất
        if self.rect.bottom + dy > Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT:
            dy = Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT - self.rect.bottom
            self.in_air = False

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