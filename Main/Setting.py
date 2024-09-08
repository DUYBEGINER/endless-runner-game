import pygame
import sys

pygame.init()

# const
SCREEN_WIDTH, SCREEN_HEIGHT = 280, 450  # kích thước màn hình setting
WHITE = (255, 255, 255)  
BUTTON_COLOR = (0, 128, 255)  # màu button
BUTTON_HOVER_COLOR = (0, 100, 200)  # màu button khi hover
FONT_SIZE = 30  # font chữ
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50  # kích thưosc button
BUTTON_SPACING = 10  # khoảng cách các button

# khởi tạo màn hình và đặt tên
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# tải ảnh nền và thay đổi kích thước cho phù hợp
bg = pygame.image.load("Asset/Setting/bg.jpg")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# tạo font chữ
font = pygame.font.Font(None, FONT_SIZE)

# hàm vẽ nút
def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()  # lấy vị trí chuột
    is_hovered = pygame.Rect(x, y, width, height).collidepoint(mouse_pos)  # kiểm tra xem chuột có đang hover vào button hay không
    
    # Chọn màu button dựa trên việc chuột có đang hover không
    button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    
    # vẽ văn bản trên button
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# hàm hiển thị menu
def menu():
    global start_button_rect, settings_button_rect, exit_button_rect
    
    # vị trí của các nút
    start_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    start_button_y = 140
    settings_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    settings_button_y = start_button_y + BUTTON_HEIGHT + BUTTON_SPACING
    exit_button_x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
    exit_button_y = settings_button_y + BUTTON_HEIGHT + BUTTON_SPACING

    # tạo các đối tượng pygame.Rect cho các button
    start_button_rect = pygame.Rect(start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    settings_button_rect = pygame.Rect(settings_button_x, settings_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_button_rect = pygame.Rect(exit_button_x, exit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # thoát game nếu đóng cửa sổ
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # nhận vị trí chuột khi click
                # kiểm tra xem chuột có click vào button nào không và thực hiện hành động tương ứng
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Start Game clicked!")
                    # thực hiện start game
                elif settings_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Settings clicked!")
                    # thực hiện mở setting
                elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()  # thoát game nếu click chuột vào nút Exit
        
        # vẽ nền
        screen.blit(bg, (0, 0))

        # vẽ các button
        draw_button("Start Game", start_button_x, start_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button("Settings", settings_button_x, settings_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button("Exit", exit_button_x, exit_button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

        # cập nhật màn hình
        pygame.display.flip()

# chạy hàm menu khi chạy chương trình
if __name__ == "__main__":
    menu()
