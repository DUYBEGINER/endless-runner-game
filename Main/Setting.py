import pygame
import pygame_menu
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ
width, height = 280,400
screen = pygame.display.set_mode((width, height))

# Đặt tiêu đề cho cửa sổ
pygame.display.set_caption("Game Menu")

# Tạo một hàm để bắt đầu trò chơi
def start_the_game():
    print("Bắt đầu trò chơi!")
    # Tại đây, bạn có thể bắt đầu vòng lặp trò chơi hoặc chuyển cảnh

# Tạo một hàm để thoát trò chơi
def exit_game():
    pygame.quit()
    sys.exit()

# Tạo một menu
menu = pygame_menu.Menu('Chào mừng đến với Game!', width, height,
                       theme=pygame_menu.themes.THEME_DARK)

# Thêm các tùy chọn vào menu
menu.add_button('Bắt đầu trò chơi', start_the_game)
menu.add_button('Thoát', exit_game)

# Vòng lặp chính của game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Làm mới màn hình
    screen.fill((0, 0, 0))

    # Hiển thị menu
    menu.mainloop(screen)

    # Cập nhật màn hình
    pygame.display.flip()
