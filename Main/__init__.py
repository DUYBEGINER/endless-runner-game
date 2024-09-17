import pygame, os, random, sys
from pygame import *
import Variables
from Variables import effect_list
import Shield
from Players import Player
import Stone_fall, Boom
import Players
import menu, Setting
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
menu_image = pygame.image.load(os.path.join(Variables.current_dir,'Asset/Setting/openmenu.png'))
menu_image = pygame.transform.scale(menu_image, (35, 35))
# Vị trí của ảnh menu
menu_image_rect = menu_image.get_rect(topleft=(10, 10))
# Background
BACKGROUND_IMG1 = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/background3.png'))
BACKGROUND_IMG1 = pygame.transform.scale(BACKGROUND_IMG1,(Variables.WINDOW_WIDTH * 1.25, Variables.WINDOW_HEIGHT * 1.25))
BACKGROUND_IMG2 = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/background1.png'))
BACKGROUND_IMG2 = pygame.transform.scale(BACKGROUND_IMG2,(Variables.WINDOW_WIDTH * 1.25, Variables.WINDOW_HEIGHT * 1.25))
# Groundư
GROUND_IMG = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/ground_new.png'))

update_time_score = pygame.time.get_ticks()
# Tư động sinh các đối tượng đá
def re_spawn_stone():
    tmp = random.randint(1, 100)  # Chọn một số ngẫu nhiên từ 1 đến 10
    if tmp <= 60:
        stone = Stone_fall.Stone(2, 'stone_fall1')
        Stone_fall.stones.add(stone)
    elif tmp <= 85:
        stone = Stone_fall.Stone(2, 'stone_fall2')
        Stone_fall.stones.add(stone)
    else:
        stone = Boom.boom(2)
        Stone_fall.stones.add(stone)
    tmp = random.randint(1, 100)
    if tmp > 90:
        shield = Shield.shield(1)
        Shield.Shield_Group.add(shield)

# Kiểm tra player có vừa mới nhảy không, nếu có thì thêm hiệu ứng
just_jump = False
sound_playing = False
update_time_broken = pygame.time.get_ticks()
# Biến trạng thái để theo dõi ảnh menu
show_menu = True
show_settings = False  
###############################################test
def button_action():
    print("Nút Menu đã được nhấn!")
########## VÒNG LẶP GAME ### #######
pygame.init()
#123
# Variables.sound_background.play(loops=-1)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  # Thoát game nếu đóng cửa sổ
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Nhận vị trí chuột khi click
            # Kiểm tra xem chuột có click vào button nào không và thực hiện hành động tương ứng
            
            if menu.start_button_rect.collidepoint(mouse_x, mouse_y):
                print("Start Game clicked!")
                show_menu = False
                Variables.mode_1player = True
                if menu_image_rect.collidepoint(mouse_x, mouse_y):
                    button_action()  
                if show_settings:
                    result = Setting.settings_menu(Variables.SCREEN, Variables.FONT)
                    if result == "resume":
                        show_settings = False
                        Variables.mode_1player = True
                    elif result == "restart":
                        show_settings = False
                        Variables.score = 0
                        Variables.mode_1player = True
                    elif result == "menu":
                        show_settings = False
                        show_menu = True
            elif menu.settings_button_rect.collidepoint(mouse_x, mouse_y):
                print("Settings clicked!")
                menu.settings_menu()
            elif menu.exit_button_rect.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                sys.exit()  # Thoát game nếu click chuột vào nút Exit
    
    if show_settings:
        Variables.SCREEN.fill((0, 0, 0))  # Xóa màn hình trước khi hiển thị cửa sổ settings

        continue

    if show_menu:
        Variables.SCREEN.blit(menu.bg, (0, 0))
        menu.draw_button("Start Game", menu.start_button_x, menu.start_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
        menu.draw_button("Settings", menu.settings_button_x, menu.settings_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
        menu.draw_button("Exit", menu.exit_button_x, menu.exit_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
        
        pygame.display.flip()
        continue
    
    # Vẽ nền
    menu.screen.blit(menu.bg, (0, 0))
    
    # Vẽ các button
    menu.draw_button("Start Game", menu.start_button_x, menu.start_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
    menu.draw_button("Settings", menu.settings_button_x, menu.settings_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
    menu.draw_button("Exit", menu.exit_button_x, menu.exit_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
    # Cập nhật màn hình
    pygame.display.flip()
    if Variables.mode_1player:
        # Create Player
        Player1 = Player(150, 150, 1, 2)

    
    while Variables.mode_1player:
        
        Variables.SCREEN.fill(Variables.BLACK)
        Variables.SCREEN.blit(BACKGROUND_IMG2, (0, 0))
        Variables.SCREEN.blit(BACKGROUND_IMG1, (0, 0))
        Variables.SCREEN.blit(GROUND_IMG, (0, Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT))
        Variables.SCREEN.blit(Variables.WALL_IMG1, (0, 0))
        Variables.SCREEN.blit(Variables.WALL_IMG2, (288, 0))
        Variables.SCREEN.blit(menu_image, menu_image_rect)

        
        
        
        # print(Variables.tmp_high_score)

        ##########################################--KHU VỰC PHỤ--#################################################
        Variables.SCREEN.blit(Variables.SUB_AREA, (320, 0))
        Variables.SUB_AREA.blit(Variables.SUB_AREA_IMG, (0, 0))
        #Hiển thị high_score
        Variables.draw_high_score(Variables.high_score,Variables.score_font,(186,145,88),90, 215)
        #Hiển thị Score
        Variables.draw_score(Variables.score, Variables.score_font, (186,145,88), Variables.score_x, 145)
        #Hiển thị text item
        Variables.draw_item_title( Variables.text_font, (121,144,78), 63 , 350 )
        # Hiển thị shield
        Variables.SUB_AREA_IMG.blit(Variables.SHIELD_IMG, (20, 370))
        Variables.draw_num_shield(Variables.quantity_shield, Variables.text_font, (197, 188, 157), 60, 380)
        if pygame.time.get_ticks() - update_time_score > 100:
            Variables.score += 1
            update_time_score = pygame.time.get_ticks()
            if Variables.score % Variables.score_up == 0:
                Variables.score_up *= 10
                Variables.score_x -=5
        #############################################################################################################

        Player1.update_animation()
        Player1.draw(Variables.SCREEN)
        Player1.move_and_jump(Variables.moving_left, Variables.moving_right)

        # Update player action
        if Player1.in_air:
            Player1.update_action(2)
        elif Variables.moving_left or Variables.moving_right:
            Player1.update_action(1)  # Run
        else:
            Player1.update_action(0)  # Idlea

        for event in pygame.event.get():
            if event == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Variables.mode_1player = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    Variables.moving_left = True
                    if not sound_playing and not Player1.in_air:
                        Variables.channel_walk.play(Variables.walking_sfx, loops=-1)
                        sound_playing = True
                if event.key == pygame.K_d:
                    Variables.moving_right = True
                    if not sound_playing and not Player1.in_air:
                        Variables.channel_walk.play(Variables.walking_sfx, loops=-1)
                        sound_playing = True
                if event.key == pygame.K_SPACE and not Player1.in_air:
                    Player1.jump = True
                    Variables.channel_jump.play(Variables.jump_sfx)
                    just_jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    Variables.moving_left = False
                    if not Variables.moving_right and not Player1.in_air:
                        Variables.channel_walk.stop()
                        sound_playing = False
                if event.key == pygame.K_d:
                    Variables.moving_right = False
                    if not Variables.moving_left and not Player1.in_air:
                        Variables.channel_walk.stop()
                        sound_playing = False

        # Cập nhật trạng thái âm thanh dựa trên các phím đang được nhấn và trạng thái bay
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_d]) and not Player1.in_air:
            if not sound_playing:
                Variables.channel_walk.play(Variables.walking_sfx, loops=-1)
                sound_playing = True
        elif not keys[pygame.K_a] and not keys[pygame.K_d] or Player1.in_air:
            if sound_playing:
                Variables.channel_walk.stop()
                sound_playing = False

        # Thêm hiệu ứng nhảy
        if just_jump == False:
            temp_posx = Player1.rect.x
            temp_posy = Player1.rect.y
        if just_jump == True:
            Variables.SCREEN.blit(effect_list[Variables.effect_jump_index], (temp_posx - 6, temp_posy + 10))
            Variables.effect_jump_index += 1
            if Variables.effect_jump_index >= len(Variables.effect_list):
                Variables.effect_jump_index = 0
                just_jump = False
        


        # Update class Stone
        if pygame.time.get_ticks() - Variables.update_time > Variables.COOLDOWN_SPAWN:
            Variables.update_time = pygame.time.get_ticks()
            re_spawn_stone()

        #effect_jump.draw(Variables.SCREEN,Player1.Animation_list[0][0])

        Stone_fall.stones.update()
        Stone_fall.stones.draw(Variables.SCREEN)

        Boom.booms_effect.update()
        Boom.booms_effect.draw(Variables.SCREEN)

        Shield.Shield_Group.update()
        Shield.Shield_Group.draw(Variables.SCREEN)

        ## đang sửa
        # Hiển thị ảnh menu nếu trạng thái show_menu là True
        if show_menu:
            Variables.SCREEN.blit(menu_image, menu_image_rect)

        #Chạy animation stone broken
        if Variables.check_collision_boom:
            Players.Boom_broken.update()
            Players.Boom_broken.draw(Variables.SCREEN)
        else:
            Players.Stone_broken.update()
            Players.Stone_broken.draw(Variables.SCREEN)


        for shield in Shield.Shield_Group:
            shield.check_collision_player(Player1)

        if Variables.is_exploi:
            Variables.Screen_shake_exploision(Variables.SCREEN, Variables.SCREEN_SHAKE)
            # if Variables.SCREEN_SHAKE <= 0:  # Khi shake hoàn tất
            #     Variables.is_exploiding = False  # Reset trạng thái d

        # vẽ hình vuông bao quanh để kiểm tra va chạm
        # for stone in Stone_fall.stones:
        #     pygame.draw.rect(Variables.SCREEN, (255, 0, 0), stone.rect, 2)
        if not Variables.mode_1player:
            Player1.kill()
            for i in Stone_fall.stones:
                i.kill()
            for i in Shield.Shield_Group:
                i.kill()
            for i in Boom.booms_effect:
                i.kill()
            Variables.score = 0
            Variables.moving_left = False
            Variables.moving_right = False
            Variables.moving_jump = False
            Variables.quantity_shield = 0

            
        pygame.display.update()
        FPS_Clock.tick(FPS)