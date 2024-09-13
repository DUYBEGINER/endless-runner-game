import pygame
import sys
import os
import Variables

pygame.init()

WHITE = (255, 255, 255)
BUTTON_WIDTH_Setting, BUTTON_HEIGHT_Setting = 200, 50

SCREEN_WIDTH, SCREEN_HEIGHT = 520, 500

# ảnh nền
bg_setting = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/bg.jpg'))
bg_setting = pygame.transform.scale(bg_setting, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Hàm vẽ nút
def draw_button(screen, font, text, x, y, width, height):
    BUTTON_COLOR = (0, 128, 255)
    BUTTON_HOVER_COLOR = (0, 100, 200)
    mouse_pos = pygame.mouse.get_pos()
    is_hovered = pygame.Rect(x, y, width, height).collidepoint(mouse_pos)
    button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)
    return pygame.Rect(x, y, width, height)  # Trả về đối tượng Rect của nút

# Hàm hiển thị menu cài đặt
def settings_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Thiết lập kích thước màn hình
    pygame.display.set_caption('Settings Menu')
    font = pygame.font.Font(None, 36)  # Điều chỉnh kích thước phông chữ

    volume = 50  # Giá trị âm lượng mặc định

    # Tính toán khoảng cách và vị trí các nút để căn giữa màn hình và phân bố đều
    num_buttons = 4
    button_spacing = 20  # Khoảng cách giữa các nút
    total_height = num_buttons * BUTTON_HEIGHT_Setting + (num_buttons - 1) * button_spacing
    start_y = (SCREEN_HEIGHT - total_height) // 2  # Vị trí bắt đầu trên trục Y để căn giữa các nút

    button_positions = [
        ("Volume: {}".format(volume), SCREEN_WIDTH // 2 - BUTTON_WIDTH_Setting // 2, start_y),
        ("Resume", SCREEN_WIDTH // 2 - BUTTON_WIDTH_Setting // 2, start_y + BUTTON_HEIGHT_Setting + button_spacing),
        ("Restart", SCREEN_WIDTH // 2 - BUTTON_WIDTH_Setting // 2, start_y + 2 * (BUTTON_HEIGHT_Setting + button_spacing)),
        ("Back to Menu", SCREEN_WIDTH // 2 - BUTTON_WIDTH_Setting // 2, start_y + 3 * (BUTTON_HEIGHT_Setting + button_spacing)),
    ]

    buttons_rects = []

    while True:
        screen.blit(bg_setting, (0, 0))  # Vẽ ảnh nền

        # Cập nhật các vị trí và vẽ các nút
        for index, (text, x, y) in enumerate(button_positions):
            # Nếu nút là "Volume", hiển thị giá trị âm lượng
            if text.startswith("Volume:"):
                text = "Volume: {}".format(volume)
            button_rect = draw_button(screen, font, text, x, y, BUTTON_WIDTH_Setting, BUTTON_HEIGHT_Setting)
            buttons_rects.append(button_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for index, button_rect in enumerate(buttons_rects):
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        text, x, y = button_positions[index]
                        if text.startswith("Volume:"):
                            volume = (volume + 10) % 110
                            print(f"Volume adjusted to {volume}")
                            # Cập nhật lại giá trị âm lượng trong button_positions
                            button_positions[0] = (
                            "Volume: {}".format(volume), SCREEN_WIDTH // 2 - BUTTON_WIDTH_Setting // 2, start_y)
                        elif text == "Resume":
                            print("Resume")
                            return  # Thoát khỏi menu cài đặt
                        elif text == "Restart":
                            print("Restart")
                        elif text == "Back to Menu":
                            print("Back to Menu")
                            return  # Thoát về menu chính

                # Xóa các nút cũ khỏi danh sách rects
            buttons_rects = []

            # Khởi động menu cài đặt
            settings_menu()
