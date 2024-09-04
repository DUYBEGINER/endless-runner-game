import pygame, sys
from pygame import *

####### ĐỊNH NGHĨA CÁC BIẾN ########
# Kích thước cửa sổ game
WINDOW_WIDTH = 840
WINDOW_HEIGHT = 850

# Thiết lập màn hình game
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))     # Thiết lập bề mặt màn hình chính
pygame.display.set_caption('Name_of_game')                          # Thiết lập tên cửa sổ game

# Thiết lập icon game
Game_icon = pygame.image.load('icon_game.jpg')
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
BLOCK_SIZE = 40         # Kích thước khối block

# Thêm các file ảnh vào đối tượng



########## VÒNG LẶP GAME ##########
pygame.init()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    SCREEN.fill(BLACK)

    pygame.display.update()
    FPS_Clock.tick(FPS)
pygame.quit()
