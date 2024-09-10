import pygame
import sys, os
import Variables


pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 280, 450  # Kích thước màn hình setting
WHITE = (255, 255, 255)
BUTTON_COLOR = (0, 128, 255)  # Màu button
BUTTON_HOVER_COLOR = (0, 100, 200)  # Màu button khi hover
FONT_SIZE = 30  # Font chữ
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50  # Kích thước button
BUTTON_SPACING = 10  # Khoảng cách các button

# Khởi tạo màn hình và đặt tên
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# Tải ảnh nền và thay đổi kích thước cho phù hợp
bg = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/bg.jpg'))
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Tạo font chữ
font = pygame.font.Font(None, FONT_SIZE)

# Hàm vẽ nút
def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()  # Lấy vị trí chuột
    is_hovered = pygame.Rect(x, y, width, height).collidepoint(mouse_pos)  # Kiểm tra xem chuột có đang hover vào button hay không
    
    # Chọn màu button dựa trên việc chuột có đang hover không
    button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    
    # Vẽ văn bản trên button
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# Hàm hiển thị menu chính
def menu():
    global start_button_rect, settings_button_rect, exit_button_rect
    
    # Vị trí của các nút
    start_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    start_button_y = 140
    settings_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    settings_button_y = start_button_y + BUTTON_HEIGHT + BUTTON_SPACING
    exit_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    exit_button_y = settings_button_y + BUTTON_HEIGHT + BUTTON_SPACING

    # Tạo các đối tượng pygame.Rect cho các button
    start_button_rect = pygame.Rect(start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    settings_button_rect = pygame.Rect(settings_button_x, settings_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Thoát game nếu đóng cửa sổ
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Nhận vị trí chuột khi click
                # Kiểm tra xem chuột có click vào button nào không và thực hiện hành động tương ứng
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Start Game clicked!")
                    # Thực hiện start game
                elif settings_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Settings clicked!")
                    settings_menu()
                elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()  # Thoát game nếu click chuột vào nút Exit
        
        # Vẽ nền
        screen.blit(bg, (0, 0))

        # Vẽ các button
        draw_button("Start Game", start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button("Settings", settings_button_x, settings_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button("Exit", exit_button_x, exit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Cập nhật màn hình
        pygame.display.flip()

# Hàm hiển thị menu cài đặt
def settings_menu():
    global volume, difficulty, skin
    volume = 50
    difficulty = 'Normal'
    skin = 'Default'

    # Danh sách các skin có sẵn
    skins = ['Default', 'Skin1', 'Skin2']

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Thoát game nếu đóng cửa sổ
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Nhận vị trí chuột khi click
                
                # Kiểm tra nút âm lượng
                if 40 <= mouse_x <= 240 and 80 <= mouse_y <= 130:
                    volume = (volume + 10) % 110  # Tăng âm lượng và quay lại 0 nếu vượt quá 100
                    print(f"Volume adjusted to {volume}")
                # Kiểm tra nút độ khó
                elif 40 <= mouse_x <= 240 and 150 <= mouse_y <= 200:
                    if difficulty == 'Easy':
                        difficulty = 'Normal'
                    elif difficulty == 'Normal':
                        difficulty = 'Hard'
                    else:
                        difficulty = 'Easy'
                    print(f"Difficulty set to {difficulty}")
                # Kiểm tra nút skin
                elif 40 <= mouse_x <= 240 and 220 <= mouse_y <= 270:
                    current_skin_index = skins.index(skin)
                    skin = skins[(current_skin_index + 1) % len(skins)]
                    print(f"Skin changed to {skin}")
                # Kiểm tra nút quay lại
                elif 40 <= mouse_x <= 240 and 290 <= mouse_y <= 340:
                    return  # Quay lại menu chính

        # Vẽ nền
        screen.blit(bg, (0, 0))
        
        # Vẽ các button
        draw_button(f"Volume: {volume}", 40, 80, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(f"Difficulty: {difficulty}", 40, 150, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(f"Skin: {skin}", 40, 220, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button("Back", 40, 290, BUTTON_WIDTH, BUTTON_HEIGHT)

        # Cập nhật màn hình
        pygame.display.flip()

# Chạy hàm menu khi chạy chương trình
if __name__ == "__main__":
    menu()
