import pygame, sys
from pygame import *
from pygame import mixer
import os

from Variables import *
from Players import Player

# Thiết lập màn hình game
     # Thiết lập bề mặt màn hình chính
pygame.display.set_caption('Name_of_game')                          # Thiết lập tên cửa sổ game

# Thiết lập icon game
Game_icon = pygame.image.load(os.path.join(current_dir, 'Asset/icon_game/icon_game.jpg'))
pygame.display.set_icon(Game_icon)

# Thiết lập FPS
FPS = 120
FPS_Clock = pygame.time.Clock()

#### Load ảnh ####
#Background
BACKGROUND_IMG1 = pygame.image.load(os.path.join(current_dir, 'Asset/Map/background3.png'))
BACKGROUND_IMG1 = pygame.transform.scale(BACKGROUND_IMG1, (WINDOW_WIDTH*1.25, WINDOW_HEIGHT*1.25))
BACKGROUND_IMG2 = pygame.image.load(os.path.join(current_dir, 'Asset/Map/background1.png'))
BACKGROUND_IMG2 = pygame.transform.scale(BACKGROUND_IMG2, (WINDOW_WIDTH*1.25, WINDOW_HEIGHT*1.25))
#Ground
GROUND_IMG = pygame.image.load(os.path.join(current_dir, 'Asset/Map/ground_new.png'))
# GROUND_IMG = pygame.transform.scale(GROUND_IMG, (WINDOW_WIDTH, GROUND_HEIGHT))

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
    SCREEN.blit(WALL_IMG1, (0, 0))
    SCREEN.blit(WALL_IMG2, (288, 0))
    Player1.update_animation()
    Player1.draw(SCREEN)
    Player1.Moving(SCREEN,moving_left,moving_right)
    Player1.Jump()
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
                walking_sfx.play()
            if event.key == pygame.K_d:
                moving_right = True
                walking_sfx.play()
            if event.key == pygame.K_SPACE  and not Player1.in_air:
                Player1.jump = True
                jump_sfx.play()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
                walking_sfx.stop()
            if event.key == pygame.K_d:
                moving_right = False
                walking_sfx.stop()


    pygame.display.update()
    FPS_Clock.tick(FPS)
pygame.quit()
