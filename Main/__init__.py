import pygame, sys
from pygame import *
import os
from Variables import *
from Players import Player

# Thiết lập màn hình game
SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))     # Thiết lập bề mặt màn hình chính
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
GROUND_IMG = pygame.image.load(os.path.join(current_dir, 'Asset/Map/Ground.png'))
GROUND_IMG = pygame.transform.scale(GROUND_IMG, (WINDOW_WIDTH, GROUND_HEIGHT))


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
    Player1.draw(SCREEN,moving_left, moving_right)

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
