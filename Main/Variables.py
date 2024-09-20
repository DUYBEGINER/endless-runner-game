import os
import pygame
import random
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
SCREEN = pygame.display.set_mode((WINDOW_WIDTH + 200, WINDOW_HEIGHT))
# Kích thước các đối tượng trong game
GROUND_HEIGHT = 64      # Chiều dày mặt đất
BLOCK_SIZE = 32         # Kích thước khối block
# Trọng lực
GRAVITY = 0.3
#Wall
WALL_IMG1 = pygame.image.load(os.path.join(current_dir, 'Asset/Map/wall3.png'))
WALL_IMG1 = pygame.transform.scale(WALL_IMG1, (32, WINDOW_HEIGHT-GROUND_HEIGHT))
WALL_RECT1 = WALL_IMG1.get_rect()
WALL_IMG2 = pygame.image.load(os.path.join(current_dir, 'Asset/Map/wall3.png'))
WALL_IMG2 = pygame.transform.scale(WALL_IMG2, (32, WINDOW_HEIGHT-GROUND_HEIGHT))
WALL_RECT2 = WALL_IMG2.get_rect()


#SHAKE EFFCT
SCREEN_SHAKE = 30
render_ofset = [0, 0]
is_exploi = False
def Screen_shake_exploision(SCREEN, SCREEN_SHAKE):
    if SCREEN_SHAKE > 0:
        SCREEN_SHAKE -= 1
    render_ofset = [0, 0]
    if SCREEN_SHAKE > 0:
        render_ofset[0] = random.randint(-4, 4)  # Rung theo chiều ngang
        render_ofset[1] = random.randint(-4, 4)  # Rung theo chiều dọc
    SCREEN.blit(SCREEN, render_ofset)

# Sub area
SUB_AREA = pygame.surface.Surface((200,500))
SUB_AREA_IMG = pygame.image.load(os.path.join(current_dir, 'Asset/Map/sub_area_main.png'))
SHIELD_IMG = pygame.image.load(os.path.join(current_dir, 'Asset/Item/Shield/0.png'))
SHIELD_IMG = pygame.transform.scale(SHIELD_IMG, (SHIELD_IMG.get_width()*1.25, SHIELD_IMG.get_height()*1.25))
STOPGAME_IMG = pygame.image.load(os.path.join(current_dir, 'Asset/Item/Stop_time/3.png'))
STOPGAME_IMG = pygame.transform.scale(STOPGAME_IMG, (STOPGAME_IMG.get_width()*1, STOPGAME_IMG.get_height()*1))

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

#SCORE file
fi = open(os.path.join(current_dir, 'Main/High_Score'), 'r')
score = 0
high_score = int(fi.read())


#FONT TEXT
pygame.font.init()
text_font = pygame.font.Font(None, 30)
score_font = pygame.font.Font(None, 40)
high_score_font = pygame.font.Font(None, 60)
score_x = 95
score_up = 10

def draw_high_score(surf,font,text_col,x,y):
    recor = font.render(f'{high_score}', True, text_col)
    surf.blit(recor, (x, y))

def draw_score(surf,font,text_col,x,y):
    score_game = font.render(f'{score}', True, text_col)
    surf.blit(score_game, (x, y ))


def draw_num_shield(font,text_col,x,y):
    img = font.render(f'x {quantity_shield}', True, text_col)
    SUB_AREA.blit(img, (x, y))

def draw_num_stopGameItem(font,text_col,x,y):
    img = font.render(f'x {quantity_STI}', True, text_col)
    SUB_AREA.blit(img, (x, y))


def draw_item_title(font,text_col,x,y):
    img = font.render(f'Item List', True, text_col)
    SUB_AREA.blit(img, (x, y))

#Các biến hành động nhân vật
moving_left = False
moving_right = False
moving_jump = False



#Số lượng vật phẩm
quantity_shield = 0
quantity_STI = 0

#Biến liên quan đến ngưng động màn hình
stop_time_activate = False
COOLDOWN_STOP = 120*3
cooldown_use = False #Ngăn không cho người dùng spam vật phẩn ngưng đọng thời gian

#Biến chạy hiệu ứng animation jump
effect_list = []
effect_stop_time_list = []
effect_jump_index = 0
effect_stop_time_index = 0
check_collision_boom = False


# Biến thực hiện các màn hình
mode_1player = False
RUNNING = True
pygame.init()


###### SFX ######
jump_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/jump.mp3'))
walking_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/walking.mp3'))
sound_background = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/sound_game.mp3'))
collect_shield_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/collect_shield.mp3'))
click_button_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/click_button.mp3'))
click_button_sfx2 = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/click_button2.mp3'))
click_button_sfx3 = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/click_button3.mp3'))
hover_button_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/hover_button.mp3'))
background_music = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/sound_game2.mp3'))
stop_time_sfx = pygame.mixer.Sound(os.path.join(current_dir, f'Asset/SFX/Stop_time.mp3'))

# countdown_boom.set_volume(0.3)
jump_sfx.set_volume(0.3)
walking_sfx.set_volume(1)
stop_time_sfx.set_volume(1)

#SFX Chanel
pygame.mixer.init()
channel_collect = pygame.mixer.Channel(0)  # Chọn kênh 0
channel_jump = pygame.mixer.Channel(1)
channel_walk = pygame.mixer.Channel(2)
channel_music = pygame.mixer.Channel(3)
Stop_time_channel = pygame.mixer.Channel(4)
# play_channel_collect = channel_collect.play(collect_shield_sfx)
# play_channel_boom = channel_countdown_boom.play(countdown_boom)
#
# stop_channel_collect = channel_collect.stop()
# stop_channel_boom = channel_boom.stop()


# Các biến liên quan đến thời gian spawn các chướng ngại vật đá
update_time = pygame.time.get_ticks()
COOLDOWN_SPAWN = 500

#Load animation dưới chân khi nhảy
for i in range(7):
    img = pygame.image.load(os.path.join(current_dir, f'Asset/character/distribute/{i}.png'))
    # img = pygame.transform.scale(img, (int((img.get_width() * scale)), (img.get_height() * scale)))
    effect_list.append(img)

#Load hiệu ứng sử dụng item stop_time
for i in range(41):
    img = pygame.image.load(os.path.join(current_dir, f'Asset/Item/Stop_time_effect/{i}.png'))
    img = pygame.transform.scale(img, (int((img.get_width() * 3)), (img.get_height() * 3)))
    effect_stop_time_list.append(img)

difficult = 1
global volume, difficulty, skin

#### Load ảnh ####
menu_image = pygame.image.load(os.path.join(current_dir,'Asset/Setting/openmenu.png'))
menu_image = pygame.transform.scale(menu_image, (50, 50))
# Vị trí của ảnh menu
menu_image_rect = menu_image.get_rect(topleft=(10, 10))