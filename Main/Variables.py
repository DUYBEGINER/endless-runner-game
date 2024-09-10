import os
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
####### ĐỊNH NGHĨA CÁC BIẾN ########
# Thiết lập đường dẫn
current_dir_tmp = os.path.dirname(os.path.abspath(__file__)) #  Đường dẫn tới ../main
current_dir = os.path.dirname(current_dir_tmp) # Đường dẫn tới ../Game_project
# Kích thước cửa sổ game
WINDOW_WIDTH = 320
WINDOW_HEIGHT = 500
RUNNING = True
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# Kích thước các đối tượng trong game
GROUND_HEIGHT = 64      # Chiều dày mặt đất
BLOCK_SIZE = 32         # Kích thước khối block
# Trọng lực
GRAVITY = 0.3
#Wall
WALL_IMG1 = pygame.image.load(os.path.join(current_dir, 'Asset/Map/wall.png'))
WALL_IMG1 = pygame.transform.scale(WALL_IMG1, (32, WINDOW_HEIGHT-GROUND_HEIGHT))
WALL_RECT1 = WALL_IMG1.get_rect()

WALL_IMG2 = pygame.image.load(os.path.join(current_dir, 'Asset/Map/wall.png'))
WALL_IMG2 = pygame.transform.scale(WALL_IMG2, (32, WINDOW_HEIGHT-GROUND_HEIGHT))
WALL_RECT2 = WALL_IMG2.get_rect()
# Update the wall rect positions
WALL_RECT1.topleft = (0, 0)
WALL_RECT2.topleft = (288, 0)

# WALL_RECT.center = (0, 0)
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
moving_jump = False

#Biến chạy hiệu ứng animation jump
effect_jump_index = 0
effect_list = []

pygame.init()
#SFX
#Jump
jump_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/jump.mp3'))
walking_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/walking.mp3'))
sound_background = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/sound_game.mp3'))


# Các biến liên quan đến thời gian spawn các chướng ngại vật đá
update_time = pygame.time.get_ticks()
COOLDOWN_SPAWN = 500
for i in range(7):
    img = pygame.image.load(os.path.join(current_dir, f'Asset/character/distribute/{i}.png'))
    # img = pygame.transform.scale(img, (int((img.get_width() * scale)), (img.get_height() * scale)))
    effect_list.append(img)