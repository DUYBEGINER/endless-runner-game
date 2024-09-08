import pygame, os, random
from pygame import *
import Variables
from Main.Variables import effect_list

from Players import Player
import Stone_fall

# Thiết lập màn hình game
     # Thiết lập bề mặt màn hình chính
pygame.display.set_caption('Name_of_game')                          # Thiết lập tên cửa sổ game

# Thiết lập icon game
Game_icon = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/icon_game/icon_game.jpg'))
pygame.display.set_icon(Game_icon)

# Thiết lập FPS
FPS = 120
FPS_Clock = pygame.time.Clock()

#### Load ảnh ####

#Background
BACKGROUND_IMG1 = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/background3.png'))
BACKGROUND_IMG1 = pygame.transform.scale(BACKGROUND_IMG1, (Variables.WINDOW_WIDTH*1.25, Variables.WINDOW_HEIGHT*1.25))
BACKGROUND_IMG2 = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/background1.png'))
BACKGROUND_IMG2 = pygame.transform.scale(BACKGROUND_IMG2, (Variables.WINDOW_WIDTH*1.25, Variables.WINDOW_HEIGHT*1.25))
#Ground
GROUND_IMG = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/ground_new.png'))
# GROUND_IMG = pygame.transform.scale(GROUND_IMG, (WINDOW_WIDTH, GROUND_HEIGHT))

# Create Player
Player1 = Player(150,150,1,3)



# Tư động sinh các đối tượng đá
def re_spawn_stone():
    tmp = random.randint(1,10) # Chọn một số ngẫu nhiên từ 1 đến 10
    if tmp <= 6:
        stone = Stone_fall.Stone(2,'stone_fall1')
    else:
        stone = Stone_fall.Stone(2,'stone_fall2')
    Stone_fall.stones.add(stone)

#Kiểm tra player có vừa mới nhảy không, nếu có thì thêm hiệu ứng
just_jump = False

########## VÒNG LẶP GAME ### #######
pygame.init()
# Variables.sound_background.play(loops=-1)
Running = True
while Running:

    Variables.SCREEN.fill(Variables.BLACK)
    Variables.SCREEN.blit(BACKGROUND_IMG2, (0, 0))
    Variables.SCREEN.blit(BACKGROUND_IMG1, (0, 0))
    Variables.SCREEN.blit(GROUND_IMG, (0, Variables.WINDOW_HEIGHT-Variables.GROUND_HEIGHT))
    Variables.SCREEN.blit(Variables.WALL_IMG1, (0, 0))
    Variables.SCREEN.blit(Variables.WALL_IMG2, (288, 0))
    Player1.update_animation()
    Player1.draw(Variables.SCREEN)
    Player1.Moving(Variables.moving_left, Variables.moving_right)
    Player1.Jump()


     #Update player action
    if Player1.in_air:
        Player1.update_action(2)
    elif Variables.moving_left or Variables.moving_right:
        Player1.update_action(1)    # Run
    else:
        Player1.update_action(0)    # Idle


    for event in pygame.event.get():
        if event.type == QUIT:
            Running = False
        # Xử lí di chuyển nhân vật khi ấn núta
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Variables.moving_left = True
                Variables.walking_sfx.play()
            if event.key == pygame.K_d:
                Variables.moving_right = True
                Variables.walking_sfx.play()
            if event.key == pygame.K_SPACE  and not Player1.in_air:
                Player1.jump = True
                Variables.jump_sfx.play()
                just_jump = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                Variables.moving_left = False
                Variables.walking_sfx.stop()
            if event.key == pygame.K_d:
                Variables.moving_right = False
                Variables.walking_sfx.stop()

    #Thêm hiệu ứng nhảy
    if just_jump == False:
        temp_posx= Player1.rect.x
        temp_posy = Player1.rect.y
    if just_jump == True:
        Variables.SCREEN.blit(effect_list[Variables.effect_jump_index], (temp_posx-6, temp_posy+10))
        Variables.effect_jump_index += 1
        if Variables.effect_jump_index >= len(Variables.effect_list):
            Variables.effect_jump_index = 0
            just_jump = False


    # Update class Stone
    if pygame.time.get_ticks() - Variables.update_time > Variables.COOLDOWN_SPAWN:
        Variables.update_time = pygame.time.get_ticks()
        re_spawn_stone()

        # effect_jump.draw(Variables.SCREEN,Player1.Animation_list[0][0])
    
    Stone_fall.stones.update()
    Stone_fall.stones.draw(Variables.SCREEN)

    # vẽ hình vuông bao quanh để kiểm tra va chạm
    for stone in Stone_fall.stones:
        pygame.draw.rect(Variables.SCREEN, (255, 0, 0), stone.rect, 2)


    pygame.display.update()
    FPS_Clock.tick(FPS)
pygame.quit()
