import pygame, os, random, sys
from pygame import *
import Variables
from Variables import effect_list
from Players import Player
import Stone_fall, Boom
import Players
import menu
import Button
import update_high_score
import Setting
import Item

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
menu_image_rect = menu_image.get_rect()
menu_image_rect.topleft = (10,10)
# Background
BACKGROUND_IMG1 = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/background3.png'))
BACKGROUND_IMG1 = pygame.transform.scale(BACKGROUND_IMG1,(Variables.WINDOW_WIDTH * 1.25, Variables.WINDOW_HEIGHT * 1.25))
BACKGROUND_IMG2 = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/background1.png'))
BACKGROUND_IMG2 = pygame.transform.scale(BACKGROUND_IMG2,(Variables.WINDOW_WIDTH * 1.25, Variables.WINDOW_HEIGHT * 1.25))

GAMEOVER_IMG = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/gameover.png'))

# Ground
GROUND_IMG = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Map/ground_new.png'))


####Load các ảnh và khởi tạo button gameover
home_button_default_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/home/Default.png'))
home_button_hover_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/home/Hover.png'))
restart_button_default_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/Restart/Default.png'))
restart_button_hover_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Button/Restart/Hover.png'))


#Khởi tạo button
home_button = Button.button(home_button_default_img,home_button_hover_img,150,400,0.8)
restart_button = Button.button(restart_button_default_img,restart_button_hover_img, 250,400,0.8)




update_time_score = pygame.time.get_ticks()
update_time_stop = pygame.time.get_ticks()
# Tư động sinh các đối tượng đád
def re_spawn_stone():
    if not game_over:
        tmp = random.randint(1, 100)  # Chọn một số ngẫu nhiên từ 1 đến 100
        if tmp <= 50:
            stone = Stone_fall.Stone(2, 'stone_fall1')
            Stone_fall.stones.add(stone)
        elif tmp <= 60:
            stone = Stone_fall.Stone(2, 'stone_fall2')
            Stone_fall.stones.add(stone)
        elif tmp <=80:
            stone = Boom.boom()
            Stone_fall.stones.add(stone)
        elif tmp <= 90:
            shield = Item.item(1,'Shield')
            Item.Item_Group.add(shield)
        else:
            STI = Item.item(1,'Stop_time')
            Item.Item_Group.add(STI)

def draw_button_image(screen, img, x, y):
    screen.blit(img, (x, y))

def draw_background():
    Variables.SCREEN.blit(BACKGROUND_IMG2, (0, 0))
    Variables.SCREEN.blit(BACKGROUND_IMG1, (0, 0))
    Variables.SCREEN.blit(GROUND_IMG, (0, Variables.WINDOW_HEIGHT - Variables.GROUND_HEIGHT))
    Variables.SCREEN.blit(Variables.WALL_IMG1, (0, 0))
    Variables.SCREEN.blit(Variables.WALL_IMG2, (288, 0))
    Variables.SCREEN.blit(menu_image, menu_image_rect)

def draw_sub_area():
    Variables.SCREEN.blit(Variables.SUB_AREA, (320, 0))
    Variables.SUB_AREA.blit(Variables.SUB_AREA_IMG, (0, 0))
    Variables.draw_high_score(Variables.SUB_AREA, Variables.score_font, (186, 145, 88), 90, 215)
    Variables.draw_score(Variables.SUB_AREA, Variables.score_font, (186, 145, 88), Variables.score_x, 145)
    Variables.draw_item_title(Variables.text_font, (121, 144, 78), 63, 350)
    Variables.SUB_AREA_IMG.blit(Variables.SHIELD_IMG, (20, 370))
    Variables.SUB_AREA_IMG.blit(Variables.STOPGAME_IMG, (20, 410))
    Variables.draw_num_shield(Variables.text_font, (197, 188, 157), 60, 380)
    Variables.draw_num_stopGameItem(Variables.text_font, (197, 188, 157), 60, 420)

def handle_menu_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Variables.RUNNING = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Nhận vị trí chuột khi click
            # Kiểm tra xem chuột có click vào button nào không và thực hiện hành động tương ứng
            if menu.start_button_rect.collidepoint(mouse_x, mouse_y):
                Variables.mode_1player = True
                show_menu= False
                Variables.click_button_sfx.play()
                if menu_image_rect.collidepoint(mouse_x, mouse_y):
                    Setting.settings_menu1() 
            elif menu.settings_button_rect.collidepoint(mouse_x, mouse_y):
                Variables.click_button_sfx.play()
                menu.settings_menu()
            elif menu.exit_button_rect.collidepoint(mouse_x, mouse_y):
                Variables.click_button_sfx.play()
                Variables.RUNNING = False
    if show_settings:
        Variables.SCREEN.fill((0, 0, 0))  # Xóa màn hình trước khi hiển thị cửa sổ settings
        draw_button_image(menu_image, menu_image_rect.x, menu_image_rect.y)
        pass

    # Vẽ nền
    menu.screen.blit(menu.bg, (0, 0))

    # Vẽ các button
    menu.draw_button("Start Game", menu.start_button_x, menu.start_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
    menu.draw_button("Settings", menu.settings_button_x, menu.settings_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
    menu.draw_button("Exit", menu.exit_button_x, menu.exit_button_y, menu.BUTTON_WIDTH, menu.BUTTON_HEIGHT)
    # Cập nhật màn hình
    pygame.display.flip()


def reset_game():
    # Player1.kill()
    Stone_fall.stones.empty()
    Item.Item_Group.empty()
    Boom.booms_effect.empty()
    Players.Stone_broken.empty()
    Players.Boom_broken.empty()

    Variables.is_exploi = False
    Variables.score = 0

    Variables.moving_left = False
    Variables.moving_right = False
    Variables.moving_jump = False
    Variables.quantity_shield = 0
    Variables.quantity_STI = 0
    Variables.jump_sfx.stop()
    Variables.walking_sfx.stop()
    Variables .collect_shield_sfx.stop()
    # Boom.exploision_sfx.stop()
    Boom.countdown_boom.stop()

def pause_game():
    Variables.is_exploi = False
    Variables.moving_left = False
    Variables.moving_right = False
    Variables.moving_jump = False
    Variables.jump_sfx.stop()
    Variables.walking_sfx.stop()
    Variables.collect_shield_sfx.stop()
    # Boom.exploision_sfx.stop()
    Boom.countdown_boom.stop()

pygame.font.init()
gameover_font = pygame.font.SysFont('Arial', 50)

#Các biến kiểm tra các sự kiện trong game
game_over = False
pause_in_game = False
restart = False

just_jump = False   # Kiểm tra player có vừa mới nhảy không, nếu có thì thêm hiệu ứng
sound_playing = False      #Kiểm tra âm thanh có đang chạy không
update_time_broken = pygame.time.get_ticks()    #Biến đặt thời gian cho hiệu ứng broken
# Biến trạng thái để theo dõi ảnh menu
menu_image_check = False
# Biến trạng thái để theo dõi ảnh menu
show_menu = True
show_settings = False  

def draw_button_image(screen, img, x, y):
    screen.blit(img, (x, y))


########## VÒNG LẶP GAME ### #######
pygame.init()
while Variables.RUNNING:
    if not restart:
    ############################### MÀN HÌNH MENU #####################################
        handle_menu_events()
    ####################################################################################

    if Variables.mode_1player:
        # Create Player
        Player1 = Player(150, 150, 1, 2)
        Variables.channel_music.play(Variables.background_music, loops=-1)

    #################################### MÀN HÌNH CHÍNH CỦA GAME ####################################
    while Variables.mode_1player:
        draw_background()
        draw_sub_area()
        Variables.SCREEN.blit(menu_image, menu_image_rect)
        # Xử lí đầu vào từ bàn phím
        for event in pygame.event.get():
            # KEY_DOWN
            if event.type == pygame.QUIT:
                Variables.RUNNING = False
                Variables.mode_1player = False
                game_over = False
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
                # Ấn phím J để sử dụng vật phẩm
                if event.key == pygame.K_ESCAPE:
                    pause_in_game = False
                if event.key == pygame.K_j and Variables.quantity_STI != 0 and not Variables.cooldown_use:
                    Variables.stop_time_activate = True
                    Variables.quantity_STI -= 1
                    Variables.cooldown_use = True  # Ngăn không cho người chơi trong lúc ngưng thời gian lại dùng thêm item
                    Variables.is_exploi = False
                    Variables.Stop_time_channel.play(Variables.stop_time_sfx)
            # KEY_UP
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
            # Xu ly nhan tin hieu chuot
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Nhận vị trí chuột khi click
                # Kiểm tra xem chuột có click vào button nào không và thực hiện hành động tương ứng
                if menu_image_rect.collidepoint(mouse_x, mouse_y):
                    pause_in_game = True

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

        ########### Nếu không pause game thì chạy như bình thường ############
        if not pause_in_game:
            #count score
            if pygame.time.get_ticks() - update_time_score > 100:
                Variables.score += 1
                update_time_score = pygame.time.get_ticks()
                if Variables.score % Variables.score_up == 0:
                    Variables.score_up *= 10
                    Variables.score_x -=5
            #Cập nhật player
            Player1.update_animation()
            Player1.move_and_jump(Variables.moving_left, Variables.moving_right)

            # Update player action
            if Player1.in_air:
                Player1.update_action(2)
            elif Variables.moving_left or Variables.moving_right:
                Player1.update_action(1)  # Run
            else:
                Player1.update_action(0)  # Idlea

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

            # Kiểm tra xem người chơi có đang dùng vật phẩm ngưng thời gian không
            if not Variables.stop_time_activate:
                #Sản sinh các vật thể trong game
                if pygame.time.get_ticks() - Variables.update_time > Variables.COOLDOWN_SPAWN:
                    Variables.update_time = pygame.time.get_ticks()
                    re_spawn_stone()

                #update hình ảnh các đối tượng game
                Stone_fall.stones.update()
                Boom.booms_effect.update(Player1.alive)
                Item.Item_Group.update()

                #Chạy animation Broken đối với stone hoặc boom tương ứng khi nhân vât chạm vào nhưng có khiên
                if Variables.check_collision_boom:
                    Players.Boom_broken.update()
                    Players.Boom_broken.draw(Variables.SCREEN)
                else:
                    Players.Stone_broken.update()
                    Players.Stone_broken.draw(Variables.SCREEN)
        ############ Nếu pause game thì sẽ không chạy khối code trên #######################


        #Xử lí khi nhân vật sử dụng vật phẩm ngưng thời gian
        if Variables.stop_time_activate and not pause_in_game:
            #Đây là khi nhân vật dùng ngưng đọng thời gian, bỏ qua phần update các vật thể trong game
            #Chạy animation đồng hồ quay
            if pygame.time.get_ticks() - update_time_stop > 800 and Variables.effect_stop_time_index < len(Variables.effect_stop_time_list):
                Variables.SCREEN.blit(Variables.effect_stop_time_list[Variables.effect_stop_time_index], (20, 30))
                Variables.effect_stop_time_index += 1
                update_time_stop_time = pygame.time.get_ticks()

            #Nếu ngừng thời gian chưa đủ 3s thì tiếp tục không cập nhật các đối tượng trong game trừ nhân vật
            Variables.COOLDOWN_STOP -= 1

            if Variables.COOLDOWN_STOP <= 0:
                #Nếu đã đủ 3 giây thì cho game tiếp tục chạy, tiếp tục cập nhật các đối tượng game phía trên
                Variables.Stop_time_channel.stop()     #Dừng âm thanh ngưng đọng thời gian
                Variables.stop_time_activate = False       #Đặt lại biến kiểm tra ngưng đọng trở lại False để tiếp tục cập nhật các đối tượng game
                Variables.cooldown_use = False              #Ngăn không cho spam phím J
                Variables.effect_stop_time_index = 0        # đặt lại index của frame chạy animation stop_time về 0
                Variables.COOLDOWN_STOP = 120*3   # số giây  = FPS * số giây muốn chạy

        #Vẽ các đối tượng game (mặc định luôn luôn vẽ)
        Player1.draw(Variables.SCREEN)
        Boom.booms_effect.draw(Variables.SCREEN)
        Stone_fall.stones.draw(Variables.SCREEN)
        Item.Item_Group.draw(Variables.SCREEN)

        # Nhặt item
        for item in Item.Item_Group:
            item.check_collision_player(Player1)

        #Hiệu ứng shake khi boom nổ
        if Variables.is_exploi:
            Variables.Screen_shake_exploision(Variables.SCREEN, Variables.SCREEN_SHAKE)


        ##################  HIỂN THỊ VÀ XỬ LÍ MENU PAUSE  ####################
        if pause_in_game:
            Variables.channel_music.stop()
            check = Setting.settings_menu1(Variables.SCREEN)
            print(check)
            if check == "resume":
                pause_in_game = False
            elif check == "restart":
                Variables.channel_music.play(Variables.background_music, loops=-1)
                reset_game()
                Player1.kill()
                Player1 = Player(150, 150, 1, 2)
                pause_in_game = False
            elif check == "menu":
                reset_game()
                restart = False   #Để hiển thị menu ngoài
                pause_in_game = False
                Variables.mode_1player = False
                Variables.channel_music.stop()


        #CHECK GAME OVER
        if not Player1.alive:
            game_over = True
            Variables.mode_1player = False
            pause_game()
            update_high_score.update_score()
            #chạy cập nhật boom để hiện lúc boom nổ to nhất, nhìn nó thật hơn
            for i in Boom.booms_effect:
                pygame.display.update(i.rect)
            break

        pygame.display.update()
        FPS_Clock.tick(FPS)


    ################################## Màn hình GAME OVER #############################################
    while game_over:
        Variables.channel_music.stop()  #Dừng nhạc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Variables.RUNNING = False
                game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Nhận vị trí chuột khi click
                # Kiểm tra xem chuột có click vào button nào không và thực hiện hành động tương ứng
                if home_button.rect.collidepoint(mouse_x, mouse_y):
                    # Variables.hover_button_sfx.play()
                    Variables.click_button_sfx3.play()
                    game_over = False
                    restart = False
                    reset_game()
                elif restart_button.rect.collidepoint(mouse_x, mouse_y):
                    Variables.mode_1player = True
                    game_over = False
                    restart = True
                    Variables.click_button_sfx3.play()
                    reset_game()

        Variables.SCREEN.blit(GAMEOVER_IMG, (100,100))  #Hiển thị bảng game_over
        home_button.draw()
        restart_button.draw()
        Variables.draw_score(Variables.SCREEN, Variables.score_font, (99, 102, 50), 240, 323)
        Variables.draw_high_score(Variables.SCREEN, Variables.high_score_font, (235, 128, 7), 210, 240)

        #Cập nhật bảng game over và các nút liên quan
        list_display_update = [GAMEOVER_IMG.get_rect(topleft=(100,100)), home_button.rect, restart_button.rect]
        pygame.display.update(list_display_update)

        #####$ Dừng màn hình game $#####
        draw_background()
        draw_sub_area()

        Boom.booms_effect.draw(Variables.SCREEN)
        Stone_fall.stones.draw(Variables.SCREEN)
        Item.Item_Group.draw(Variables.SCREEN)

pygame.quit()