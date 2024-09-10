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


# Ảnh shield
SHIELD_IMG = pygame.image.load(os.path.join(current_dir, 'Asset/Item/Shield/0.png'))

# Update the wall rect positions
WALL_RECT1.topleft = (0, 0)
WALL_RECT2.topleft = (288, 0)


# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
#........

#TEXT

#FONT TEXT
pygame.font.init()
text_font = pygame.font.Font(None, 30)
score = 0

def draw_text(text,font,text_col,x,y):
    img = font.render(f'score: {score}', True, text_col)
    SCREEN.blit(img, (x, y))
def draw_num_shield(text,font,text_col,x,y):
    img = font.render(f'{quantity_shield}', True, text_col)
    SCREEN.blit(img, (x, y))


#Các biến hành động nhân vật
moving_left = False
moving_right = False
moving_jump = False
quantity_shield = 0


#Biến chạy hiệu ứng animation jump
effect_list = []
effect_jump_index = 0

#Biến chạy hiệu ứng animation broken
stone_broken_animation = []
stone_broken_index = 0
pygame.init()


#SFX
jump_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/jump.mp3'))
walking_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/walking.mp3'))
sound_background = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/sound_game.mp3'))
collect_shield_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/collect_shield.mp3'))

# countdown_boom.set_volume(0.3)
jump_sfx.set_volume(0.3)
walking_sfx.set_volume(1)
#SFX Chanel
pygame.mixer.init()
channel_collect = pygame.mixer.Channel(0)  # Chọn kênh 0
channel_jump = pygame.mixer.Channel(1)
channel_walk = pygame.mixer.Channel(2)

# play_channel_collect = channel_collect.play(collect_shield_sfx)
# play_channel_boom = channel_countdown_boom.play(countdown_boom)
#
# stop_channel_collect = channel_collect.stop()
# stop_channel_boom = channel_boom.stop()


# Các biến liên quan đến thời gian spawn các chướng ngại vật đá
update_time = pygame.time.get_ticks()
COOLDOWN_SPAWN = 500
for i in range(7):
    img = pygame.image.load(os.path.join(current_dir, f'Asset/character/distribute/{i}.png'))
    # img = pygame.transform.scale(img, (int((img.get_width() * scale)), (img.get_height() * scale)))
    effect_list.append(img)

for i in range(20):
    img = pygame.image.load(os.path.join(current_dir, f'Asset/map/animation_broken/{i}.png'))

    img = pygame.transform.scale(img, (int((img.get_width() * 2)), (img.get_height() * 2)))
    stone_broken_animation.append(img)