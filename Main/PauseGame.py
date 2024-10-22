from os import write
import pygame
import sys, os
import Variables, Menu
tmp = ''
# Constants
WHITE = (255, 255, 255)

# Load button images
resume_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/resume.png'))
resume_img = pygame.transform.scale(resume_img, (int(resume_img.get_width() * 0.75), int(resume_img.get_height() * 0.75)))
restart_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/restart.png'))
restart_img = pygame.transform.scale(restart_img, (int(restart_img.get_width() * 0.75), int(restart_img.get_height() * 0.75)))
back_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/back_menu.png'))
back_img = pygame.transform.scale(back_img, (int(back_img.get_width() * 0.75), int(back_img.get_height() * 0.75)))
bg1_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/bg1.png'))
bg1_img = pygame.transform.scale(bg1_img, (int(bg1_img.get_width() * 2.5), int(bg1_img.get_height() * 2.5)))

resume_rect = pygame.Rect(40, 200, resume_img.get_width(), resume_img.get_height())
restart_rect = pygame.Rect(120, 200, restart_img.get_width(), restart_img.get_height())
back_to_menu_rect = pygame.Rect(200, 200, back_img.get_width(), back_img.get_height())

pygame.font.init()
pause_game_text = pygame.font.Font(None, 50)



def draw_button_image(screen, img, x, y):
    screen.blit(img, (x, y))

def settings_menu1(screen):
    # Button positions
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if resume_rect.collidepoint(mouse_x, mouse_y):
                    return "resume"
                    break
                elif restart_rect.collidepoint(mouse_x, mouse_y):
                    return "restart"
                    break
                elif back_to_menu_rect.collidepoint(mouse_x, mouse_y):
                    return "menu"
                    break

        # Draw the background
        #screen.blit(pygame.image.load(os.path.join(Variables.current_dir, 'Asset/gameover.png')), (0, 0))
        screen.blit(bg1_img, (0, 0))
        screen.blit(pause_game_text.render("PAUSE GAME",True,WHITE),(50,100))
        # Draw buttons
        draw_button_image(screen, resume_img, resume_rect.x, resume_rect.y)
        draw_button_image(screen, restart_img, restart_rect.x, restart_rect.y)
        draw_button_image(screen, back_img, back_to_menu_rect.x, back_to_menu_rect.y)
    
        pygame.display.flip()

# def handle_settings_action(action):
#     if action == "resume":
#         print("Game Resumed")  # Thực hiện hành động khôi phục trò chơi
#         return False  # Quay lại trò chơi
#     elif action == "restart":
#         print("Game Restarted")  # Thực hiện hành động khởi động lại trò chơi
#         return True  # Quay lại trò chơi và khởi động lại
#     elif action == "menu":
#         print("Returning to Main Menu")  # Quay lại menu chính
#         return "menu"  # Quay lại menu chính
