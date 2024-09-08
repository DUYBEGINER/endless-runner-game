import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 280, 450  # kích thước màn hình setting
WHITE = (255, 255, 255)  
BUTTON_COLOR = (0, 128, 255)  
BUTTON_HOVER_COLOR = (0, 100, 200)  # màu của nút khi hover
FONT_SIZE = 30  # font chữ
BUTTON_WIDTH, BUTTON_HEIGHT = 200,50  # kích thước nút
BUTTON_SPACING = 10  # khoảng cách giữa các nút

# khởi tạo màn hình và đặt tiêu đề
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu")

# tải ảnh nền
bg = pygame.image.load("Asset/Setting/bg.jpg")
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# tạo font chữ
font = pygame.font.Font(None, FONT_SIZE)

# hàm vẽ nút
def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()  # lấy vị trí chuột
    is_hovered = pygame.Rect(x, y, width, height).collidepoint(mouse_pos)  # kiểm tra xem chuột có đang hover vào nút không
    
    # chọn màu nút dựa trên việc chuột có đang hover không
    button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_COLOR
    pygame.draw.rect(screen, button_color, (x, y, width, height))
    
    # vẽ văn bản trên nút
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

# hàm hiển thị menu
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  #thoát trò chơi nếu người dùng đóng cửa sổ
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()  # Lấy vị trí chuột khi nhấp
                # kiểm tra xem chuột có nhấp vào nút nào không và thực hiện hành động tương ứng
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Start Game clicked!")
                    # thực hiện hành động bắt đầu trò chơi
                elif settings_button_rect.collidepoint(mouse_x, mouse_y):
                    print("Settings clicked!")
                    # thực hiện hành động mở cài đặt
                elif exit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()  # thoát trò chơi nếu người dùng nhấp vào nút Exit
        
        # vẽ nền
        screen.blit(bg, (0, 0))

        # vẽ nút
        draw_button("Start Game", (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 100, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button("Settings", (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 100 + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button("Exit", (SCREEN_WIDTH - BUTTON_WIDTH) // 2, 100 + 2 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT)

        # update màn hình
        pygame.display.flip()

# chạy hàm menu khi chạy chương trình
if __name__ == "__main__":
    menu()
