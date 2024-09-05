import pygame, sys
from pygame import *
import os

current_dir_tmp = os.path.dirname(os.path.abspath(__file__)) # đường dẫn tới ../Main
current_dir = os.path.dirname(os.path.abspath(current_dir_tmp)) # đường dẫn tới ../GAME_PROJECT


####### ĐỊNH NGHĨA CÁC BIẾN ########
# Kích thước cửa sổ game
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 500

# Thiết lập màn hình game
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))     # Thiết lập bề mặt màn hình chính
pygame.display.set_caption('Name_of_game')                          # Thiết lập tên cửa sổ game

# Thiết lập icon game
Game_icon = pygame.image.load(os.path.join(current_dir, 'Asset/icon_game/icon_game.jpg'))
pygame.display.set_icon(Game_icon)

# Thiết lập FPS
FPS = 120
FPS_Clock = pygame.time.Clock()


# Kích thước các đối tượng trong game
GROUND_HEIGHT = 64      # Chiều dày mặt đất
BLOCK_SIZE = 32         # Kích thước khối block
# Trọng lực
GRAVITY = 0.25

#### Load ảnh ####
#Background
BACKGROUND_IMG1 = pygame.image.load(os.path.join(current_dir, 'Asset/Map/background3.png'))
BACKGROUND_IMG1 = pygame.transform.scale(BACKGROUND_IMG1, (WINDOW_WIDTH*1.25, WINDOW_HEIGHT*1.25))
BACKGROUND_IMG2 = pygame.image.load(os.path.join(current_dir, 'Asset/Map/background1.png'))
BACKGROUND_IMG2 = pygame.transform.scale(BACKGROUND_IMG2, (WINDOW_WIDTH*1.25, WINDOW_HEIGHT*1.25))
#Ground
GROUND_IMG = pygame.image.load(os.path.join(current_dir, 'Asset/Map/Ground.png'))
GROUND_IMG = pygame.transform.scale(GROUND_IMG, (WINDOW_WIDTH, GROUND_HEIGHT))


# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#........

#Các biến hành động nhân vật
moving_left = False
moving_right = False



#Các đối tượng trong game
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
            num_of_frames = len(os.listdir(os.path.join(current_dir, f'Asset/character/{animation}')))
            for i in range(num_of_frames):
                img = pygame.image.load(os.path.join(current_dir, f'Asset/character/{animation}/{i}.png'))
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
    def draw(self):
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


# Create Player
Player1 = Player(150,400,1,2)


########## VÒNG LẶP GAME ### #######
pygame.init()
Running = True
while Running:
    SCREEN.fill(BLACK)
    SCREEN.blit(BACKGROUND_IMG2, (0, 0))
    SCREEN.blit(BACKGROUND_IMG1, (0, 0))
    SCREEN.blit(GROUND_IMG, (0, WINDOW_HEIGHT-GROUND_HEIGHT))
    Player1.update_animation()
    Player1.draw()

    #Update player action
    if Player1.in_air:
        Player1.update_action(2)
    elif moving_left or moving_right:
        Player1.update_action(1)    # Run
    else:
        Player1.update_action(0)    #Idle

    for event in pygame.event.get():
        if event.type == QUIT:
            Running = False
        # Xử lí di chuyển nhân vật khi ấn nút
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                Player1.jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False


    pygame.display.update()
    FPS_Clock.tick(FPS)
pygame.quit()
