import pygame
import sys

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước màn hình và các màu sắc
screen_width, screen_height = 320,500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

#màu
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Thiết lập font chữ
font = pygame.font.SysFont(None, 35)

# Hàm vẽ văn bản
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Hàm hiển thị menu
def show_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Main Menu', font, BLACK, screen, screen_width // 2, screen_height // 4)
        draw_text('Start Game', font, BLUE, screen, screen_width // 2, screen_height // 2 - 30)
        draw_text('Quit', font, RED, screen, screen_width // 2, screen_height // 2 + 30)
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if screen_width // 2 - 100 < mouse_pos[0] < screen_width // 2 + 100 and screen_height // 2 - 60 < mouse_pos[1] < screen_height // 2 - 10:
                    return  # Quay lại màn hình chính (hoặc bắt đầu trò chơi)
                elif screen_width // 2 - 100 < mouse_pos[0] < screen_width // 2 + 100 and screen_height // 2 + 10 < mouse_pos[1] < screen_height // 2 + 60:
                    pygame.quit()
                    sys.exit()

# Hàm main
def main_game():
    while True:
        screen.fill(WHITE)
        draw_text('Game Screen', font, BLACK, screen, screen_width // 2, screen_height // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Thêm logic trò chơi ở đây

# Chạy chương trình
show_menu()
main_game()

