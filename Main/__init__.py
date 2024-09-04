import pygame, sys
from pygame import *


####### ĐỊNH NGHĨA CÁC BIẾN ########
# Kích thước cửa sổ game
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 500

# Thiết lập màn hình game
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))     # Thiết lập bề mặt màn hình chính
pygame.display.set_caption('Name_of_game')                          # Thiết lập tên cửa sổ game

# Thiết lập icon game
Game_icon = pygame.image.load('Asset/icon_game.jpg')
pygame.display.set_icon(Game_icon)

# Thiết lập FPS
FPS = 120
FPS_Clock = pygame.time.Clock()


# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#........


# Kích thước các đối tượng trong game
GROUND_HEIGHT = 50      # Chiều dày mặt đất
BLOCK_SIZE = 80         # Kích thước khối block

#Các biến hành động nhân vật
moving_left = False
moving_right = False


#Load ảnh các đối tượng tron ggme
# Player_img = pygame.image.load('Asset/character/Idle/char_animation0.png')

#Các đối tượng trong game
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y,scale,speed):
        super().__init__()
        #Animation idle
        self.Animation_list = []
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(6):
            img = pygame.image.load(f'Asset/character/Idle/char_animation{i}.png')
            img = pygame.transform.scale(img, (int((img.get_width() * scale)), (img.get_height() * scale)))
            self.Animation_list.append(img)
        self.image = self.Animation_list[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        #Các biến dùng để di chuyển, biến đổi
        self.speed = speed
        self.flip = False       #Kiểm tra lật qua lại
        # self.direction = 1


    def moving(self,moving_left,moving_right):
        #Reset biến tọa độ
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

        #Update position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        self.moving(moving_left, moving_right)
        SCREEN.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.Animation_list[self.index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            if self.index>= len(self.Animation_list)-1:
                self.index = 0
            self.update_time = pygame.time.get_ticks()
            self.image = self.Animation_list[self.index]
            self.index += 1

#Object group
#Player
Player1 = Player(100,100,1,5)



########## VÒNG LẶP GAME ### #######
pygame.init()
Running = True
while Running:
    SCREEN.fill(BLACK)
    for event in pygame.event.get():
        if event.type == QUIT:
            Running = False
        # Xử lí di chuyển nhân vật khi ấn nút
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False


    Player1.update_animation()
    Player1.draw()


    pygame.display.update()
    FPS_Clock.tick(FPS)
pygame.quit()
