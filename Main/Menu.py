if __name__ == "__main__":
    menu()

#setting trong khi chơi game
# settings.py
import pygame
import sys, os
import Variables

# Constants
WHITE = (255, 255, 255)
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50

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

def settings_menu(screen, font):
    volume = 50
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 60 <= mouse_x <= 260 and 80 <= mouse_y <= 130:  # Volume button
                    volume = (volume + 10) % 110
                    print(f"Volume adjusted to {volume}")
                elif 60 <= mouse_x <= 260 and 150 <= mouse_y <= 200:  # Resume button
                    return "resume"
                elif 60 <= mouse_x <= 260 and 220 <= mouse_y <= 270:  # Restart button
                    return "restart"
                elif 60 <= mouse_x <= 260 and 290 <= mouse_y <= 340:  # Exit button
                    return "menu"

        screen.blit(pygame.image.load(os.path.join(current_dir, 'GAME_PROJECT/Asset/Setting/bg.jpg')), (0, 0))
        draw_button(screen, font, f"Volume: {volume}", 60, 80, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(screen, font, "Resume", 60, 150, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(screen, font, "Restart", 60, 220, BUTTON_WIDTH, BUTTON_HEIGHT)
        draw_button(screen, font, "Back to Menu", 60, 290, BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.display.flip()