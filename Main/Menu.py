import pygame
import sys, os
import Variables ,  json

pygame.init()

# Constants
SCREEN_WIDTH_MENU, SCREEN_HEIGHT_MENU = 520, 500  # Kích thước màn hình
WHITE = (255, 255, 255)
BUTTON_COLOR = (0, 128, 255)  # Màu button
BUTTON_HOVER_COLOR = (0, 100, 200)  # Màu button khi hover
FONT_SIZE = 35  # Font chữ lớn hơn
BUTTON_WIDTH, BUTTON_HEIGHT = 220, 50  # Kích thước button
BUTTON_SPACING = 15  # Khoảng cách các button
SETTINGS_FILE = 'settings.json'  # Tên tệp lưu trữ cài đặt

# Khởi tạo màn hình và đặt tên
screen = pygame.display.set_mode((SCREEN_WIDTH_MENU, SCREEN_HEIGHT_MENU))
pygame.display.set_caption("Menu")

# Tải ảnh nền và thay đổi kích thước cho phù hợp
bg = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/backgroundnew2.png'))
bg = pygame.transform.scale(bg, (SCREEN_WIDTH_MENU, SCREEN_HEIGHT_MENU))

# Tạo font chữ
font = pygame.font.Font(None, FONT_SIZE)
was_hover = False
# Hàm vẽ nút
def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột
    is_hovered = pygame.Rect(x, y, width, height).collidepoint(mouse_pos)  # Kiểm tra xem chuột có đang hover vào button hay không
    
    # Chọn màu button dựa trên việc chuột có đang hover không
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect_surface.fill((0, 128, 255, 250)) if is_hovered else rect_surface.fill((0, 100, 200, 200))
    # pygame.draw.rect(screen, button_color, (x, y, width, height))


    Variables.SCREEN.blit(rect_surface, (x, y))
    # Vẽ văn bản trên button
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Hàm đọc cài đặt từ tệp JSON
def read_settings():
    global volume, difficulty, skin
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            difficulty = settings.get('difficulty', 'Easy')
            skin = settings.get('skin', 'WHITE')
            volume = settings.get('volume', 'Yes')
           
    else:
        set_default_settings()

def set_default_settings():
    global volume, difficulty, skin
    difficulty = 'Easy'
    skin = 'WHITE'
    volume = 'Yes'

# Hàm ghi cài đặt vào tệp JSON
def write_settings():
    global volume, difficulty, skin
    settings = {
        'difficulty': difficulty,
        'skin': skin,
        'volume': volume
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

# Hàm hiển thị menu chính

global start_button_rect, settings_button_rect, exit_button_rect

# Vị trí của các nút
start_button_x = (SCREEN_WIDTH_MENU - BUTTON_WIDTH) // 2
start_button_y = SCREEN_HEIGHT_MENU // 2 - 1.5 * BUTTON_HEIGHT - BUTTON_SPACING
settings_button_x = (SCREEN_WIDTH_MENU - BUTTON_WIDTH) // 2
settings_button_y = start_button_y + BUTTON_HEIGHT + BUTTON_SPACING
exit_button_x = (SCREEN_WIDTH_MENU - BUTTON_WIDTH) // 2
exit_button_y = settings_button_y + BUTTON_HEIGHT + BUTTON_SPACING

# Tạo các đối tượng pygame.Rect cho các button
start_button_rect = pygame.Rect(start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
settings_button_rect = pygame.Rect(settings_button_x, settings_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()  # Thoát game nếu đóng cửa sổ
#         elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             mouse_x, mouse_y = pygame.mouse.get_pos()  # Nhận vị trí chuột khi click
#             # Kiểm tra xem chuột có click vào button nào không và thực hiện hành động tương ứng
#             if start_button_rect.collidepoint(mouse_x, mouse_y):
#                 print("Start Game clicked!")
#                 # Thực hiện start game
#             elif settings_button_rect.collidepoint(mouse_x, mouse_y):
#                 print("Settings clicked!")
#                 settings_menu()
#             elif exit_button_rect.collidepoint(mouse_x, mouse_y):
#                 pygame.quit()
#                 sys.exit()  # Thoát game nếu click chuột vào nút Exit
#     # Vẽ nền
#     screen.blit(bg, (0, 0))
#     # Vẽ các button
#     draw_button("Start Game", start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
#     draw_button("Settings", settings_button_x, settings_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
#     draw_button("Exit", exit_button_x, exit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

#     # Cập nhật màn hình
#     pygame.display.flip()

def mute_all_sounds():
    pygame.mixer.stop()  # Dừng tất cả âm thanh hiện tại
    pygame.mixer.music.stop()  # Dừng nhạc nền
    pygame.mixer.set_num_channels(0)  # Tắt tất cả các kênh âm thanh
def unmute_all_sounds():
    pygame.mixer.set_num_channels(8)  # Mở lại một số kênh âm thanh
    pygame.mixer.music.set_volume(1)  # Đặt âm lượng tối đa

# Hàm hiển thị menu cài đặt
def settings_menu():
    global volume, difficulty, skin
    read_settings()  # Đọc cài đặt từ tệp khi vào menu cài đặt
    

    # Danh sách các skin có sẵn
    skins = ['WHITE', 'BLACK']

    # Tải ảnh nền và thay đổi kích thước cho phù hợp
    bg = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/backgroundnew2.png'))
    bg = pygame.transform.scale(bg, (SCREEN_WIDTH_MENU, SCREEN_HEIGHT_MENU))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Thoát game nếu đóng cửa sổ
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Nhận vị trí chuột khi click
                # Kiểm tra nút âm lượng
                if 50 <= mouse_x <= 270 and 80 <= mouse_y <= 130:
                    Variables.click_button_sfx3.play()
                    if volume == 'Yes':
                        volume = 'No'
                        mute_all_sounds()
                    else:
                        volume = 'Yes'
                        unmute_all_sounds()  # Mở lại âm thanh

                # Kiểm tra nút độ khó
                elif 50 <= mouse_x <= 270 and 150 <= mouse_y <= 200 and skin != 'BLACK':
                    Variables.click_button_sfx2.play()
                    if difficulty == 'Easy':
                        difficulty = 'Normal'
                        Variables.list_rate = [60, 70, 95, 98, 'Normal']
                    elif difficulty == 'Normal':
                        difficulty = 'Hard'
                        Variables.list_rate = [50, 60, 95, 98, 'Hard']
                    elif difficulty == 'Hard':
                        difficulty = 'Easy'
                        Variables.list_rate = [60, 75, 90, 95, 'Easy']
                # Kiểm tra nút skin
                elif 50 <= mouse_x <= 270 and 220 <= mouse_y <= 270:
                    Variables.click_button_sfx.play()
                    current_skin_index = skins.index(skin)
                    skin = skins[(current_skin_index + 1) % len(skins)]
                    print(f"Skin changed to {skin}")
                    if skin == 'BLACK':
                        difficulty = 'Hardest'
                        Variables.list_rate = [40, 55, 97, 99, 'Hardest']
                    else:
                        difficulty = 'Easy'
                        Variables.list_rate = [60, 75, 90, 95, 'Easy']
                # Kiểm tra nút quay lại
                elif 50 <= mouse_x <= 270 and 290 <= mouse_y <= 340:
                    Variables.click_button_sfx.play()
                    write_settings()
                    return  # Quay lại menu chính

        # Vẽ nền
        screen.blit(bg, (0, 0))
        
        # Vẽ các button
        draw_button(f"Volume: {volume}", 50, 80, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(f"Difficulty: {difficulty}", 50, 150, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(f"Skin: {skin}", 50, 220, BUTTON_WIDTH, BUTTON_HEIGHT)  # Hiển thị skin hiện tại
        draw_button("Back", 50, 290, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Cập nhật màn hình
        pygame.display.flip()