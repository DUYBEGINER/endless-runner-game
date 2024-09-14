import pygame, os, random, sys
from pygame import *
import Variables
from Variables import effect_list
import Shield
from Players import Player
import Stone_fall, Boom
import Players
import menu
import Button
import update_high_score



# Thiết lập màn hình game
# Thiết lập bề mặt màn hình chính
pygame.display.set_caption('Name_of_game')  # Thiết lập tên cửa sổ game

# Thiết lập icon game
Game_icon = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/icon_game/icon_game.jpg'))
pygame.display.set_icon(Game_icon)

# Thiết lập FPS
FPS = 120
FPS_Clock = pygame.time.Clock()

#### Load ảnh ####
# Background
BACKGROUND_IMG1 = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/background3.png'))
BACKGROUND_IMG1 = pygame.transform.scale(BACKGROUND_IMG1,(Variables.WINDOW_WIDTH_MODE2 * 1.25, Variables.WINDOW_HEIGHT_MODE2 * 1.25))
BACKGROUND_IMG2 = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/background1.png'))
BACKGROUND_IMG2 = pygame.transform.scale(BACKGROUND_IMG2,(Variables.WINDOW_WIDTH_MODE2 * 1.25, Variables.WINDOW_HEIGHT_MODE2 * 1.25))

GAMEOVER_IMG = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/gameover.png'))
# HOME_BUTTON_IMG = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/home/Default.png')).convert_alpha()
home_button_default_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/home/Default.png'))
home_button_hover_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/home/Hover.png'))
restart_button_default_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/Restart/Default.png'))
restart_button_hover_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/Restart/Hover.png'))
restart = False

home_button = Button.button(home_button_default_img,home_button_hover_img,150,400,0.8)
restart_button = Button.button(restart_button_default_img,restart_button_hover_img, 250,400,0.8)
# Ground
GROUND_IMG = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/ground_new.png'))
pause = False

update_time_score = pygame.time.get_ticks()
# Tư động sinh các đối tượng đád
def re_spawn_stone_mode2():
    if not pause:
        tmp = random.randint(1, 100)  # Chọn một số ngẫu nhiên từ 1 đến 10
        if tmp <= 50:
            stone = Stone_fall.Stone(2, 'stone_fall1', 'mode2')
            Stone_fall.stones.add(stone)
            stone = Stone_fall.Stone(2, 'stone_fall1', 'mode3')
            Stone_fall.stones.add(stone)
        elif tmp <= 75:
            stone = Stone_fall.Stone(2, 'stone_fall2', 'mode2')
            Stone_fall.stones.add(stone)
            stone = Stone_fall.Stone(2, 'stone_fall2', 'mode3')
            Stone_fall.stones.add(stone)
        else:
            stone = Boom.boom(2, 'mode2')
            Stone_fall.stones.add(stone)
            stone = Boom.boom(2, 'mode3')
            Stone_fall.stones.add(stone)
        tmp = random.randint(1, 100)
        if tmp > 90:
            shield = Shield.shield(1, 'mode2')
            Shield.Shield_Group.add(shield)
            shield = Shield.shield(1, 'mode3')
            Shield.Shield_Group.add(shield)

def draw_background():
    Variables.SCREEN_MODE2.blit(BACKGROUND_IMG2, (0, 0))
    Variables.SCREEN_MODE2.blit(BACKGROUND_IMG1, (0, 0))
    Variables.SCREEN_MODE2.blit(GROUND_IMG, (0, Variables.WINDOW_HEIGHT_MODE2 - Variables.GROUND_HEIGHT))
    Variables.SCREEN_MODE2.blit(GROUND_IMG, (256, Variables.WINDOW_HEIGHT_MODE2 - Variables.GROUND_HEIGHT))
    Variables.SCREEN_MODE2.blit(Variables.WALL_IMG1, (0, 0))
    Variables.SCREEN_MODE2.blit(Variables.WALL_IMG1, (256, 0))
    Variables.SCREEN_MODE2.blit(Variables.WALL_IMG2, (224, 0))
    Variables.SCREEN_MODE2.blit(Variables.WALL_IMG2, (480, 0))
def draw_sub_area():
    Variables.SCREEN.blit(Variables.SUB_AREA, (512, 0))
    Variables.SUB_AREA.blit(Variables.SUB_AREA_IMG, (0, 0))
    Variables.draw_high_score(Variables.high_score, Variables.score_font, (186, 145, 88), 90, 215)
    Variables.draw_score(Variables.score, Variables.score_font, (186, 145, 88), Variables.score_x, 145)
    Variables.draw_item_title(Variables.text_font, (121, 144, 78), 63, 350)
    Variables.SUB_AREA_IMG.blit(Variables.SHIELD_IMG, (20, 370))
    Variables.draw_num_shield(Variables.quantity_shield, Variables.text_font, (197, 188, 157), 60, 380)

# Kiểm tra player có vừa mới nhảy không, nếu có thì thêm hiệu ứng
just_jump = False
sound_playing = False
update_time_broken = pygame.time.get_ticks()
Player1 = Player(150, 150, 1, 2, 'mode2')
Player2 = Player(406, 150, 1, 2, 'mode2')
#####################################################333
while Variables.RUNNING:
    draw_background()
    #Cập nhật player
    Player1.update_animation()
    Player1.draw(Variables.SCREEN)
    Player1.move_and_jump(Variables.moving_left_pl1, Variables.moving_right_pl1)
    # Update player action
    if Player1.in_air:
        Player1.update_action(2)
    elif Variables.moving_left_pl1 or Variables.moving_right_pl1:
        Player1.update_action(1)  # Run
    else:
        Player1.update_action(0)  # Idlea

    Player2.update_animation()
    Player2.draw(Variables.SCREEN)
    Player2.move_and_jump(Variables.moving_left_pl2, Variables.moving_right_pl2)

    # Update player action
    if Player2.in_air:
        Player2.update_action(2)
    elif Variables.moving_left_pl2 or Variables.moving_right_pl2:
        Player2.update_action(1)  # Run
    else:
        Player2.update_action(0)  # Idlea


    #Xử lí đầu vào từ bàn phím
    for event in pygame.event.get():
        #KEY_DOWN
        # Player 1
        if event.type == pygame.QUIT:
            Variables.RUNNING = False
        if event == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                Variables.mode_1player = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                Variables.moving_left_pl1 = True
                if not sound_playing and not Player1.in_air:
                    Variables.channel_walk.play(Variables.walking_sfx, loops=-1)
                    sound_playing = True
            if event.key == pygame.K_d:
                Variables.moving_right_pl1 = True
                if not sound_playing and not Player1.in_air:
                    Variables.channel_walk.play(Variables.walking_sfx, loops=-1)
                    sound_playing = True
            if event.key == pygame.K_SPACE and not Player1.in_air:
                Player1.jump = True
                Variables.channel_jump.play(Variables.jump_sfx)
                just_jump = True

            # Player 2
            if event.key == pygame.K_LEFT:
                Variables.moving_left_pl2 = True
                if not sound_playing and not Player1.in_air:
                    Variables.channel_walk.play(Variables.walking_sfx, loops=-1)
                    sound_playing = True
            if event.key == pygame.K_RIGHT:
                Variables.moving_right_pl2 = True
                if not sound_playing and not Player1.in_air:
                    Variables.channel_walk.play(Variables.walking_sfx, loops=-1)
                    sound_playing = True
            if event.key == pygame.K_KP_ENTER and not Player1.in_air:
                Player2.jump = True
                Variables.channel_jump.play(Variables.jump_sfx)
                just_jump = True
        #KEY_UP
        if event.type == pygame.KEYUP:
            # Player 1
            if event.key == pygame.K_a:
                Variables.moving_left_pl1 = False
                if not Variables.moving_right_pl1 and not Player1.in_air:
                    Variables.channel_walk.stop()
                    sound_playing = False
            if event.key == pygame.K_d:
                Variables.moving_right_pl1 = False
                if not Variables.moving_left_pl1 and not Player1.in_air:
                    Variables.channel_walk.stop()
                    sound_playing = False
            # Player 2
            if event.key == pygame.K_LEFT:
                Variables.moving_left_pl2 = False
                if not Variables.moving_right_pl2 and not Player2.in_air:
                    Variables.channel_walk.stop()
                    sound_playing = False
            if event.key == pygame.K_RIGHT:
                Variables.moving_right_pl2 = False
                if not Variables.moving_left_pl2 and not Player2.in_air:
                    Variables.channel_walk.stop()
                    sound_playing = False
    # Update class Stone
    if pygame.time.get_ticks() - Variables.update_time > Variables.COOLDOWN_SPAWN:
        Variables.update_time = pygame.time.get_ticks()
        re_spawn_stone_mode2()
    Stone_fall.stones.update()
    Stone_fall.stones.draw(Variables.SCREEN)

    Boom.booms_effect.update()
    Boom.booms_effect.draw(Variables.SCREEN)

    Shield.Shield_Group.update()
    Shield.Shield_Group.draw(Variables.SCREEN)

    pygame.display.update()
    FPS_Clock.tick(FPS)
pygame.quit()