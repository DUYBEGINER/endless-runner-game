import pygame
import sys, os
import Variables, menu
tmp = ''
# Constants
WHITE = (255, 255, 255)

# Load button images
resume_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/resume.png'))
resume_img = pygame.transform.scale(resume_img, (int(resume_img.get_width() * 0.2), int(resume_img.get_height() * 0.2)))
restart_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/restart.png'))
restart_img = pygame.transform.scale(restart_img, (int(restart_img.get_width() * 0.2), int(restart_img.get_height() * 0.2)))
back_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/back_menu.png'))
back_img = pygame.transform.scale(back_img, (int(back_img.get_width() * 0.2), int(back_img.get_height() * 0.2)))

resume_rect = pygame.Rect(60, 150, resume_img.get_width(), resume_img.get_height())
restart_rect = pygame.Rect(60, 220, restart_img.get_width(), restart_img.get_height())
back_to_menu_rect = pygame.Rect(60, 290, back_img.get_width(), back_img.get_height())

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
                elif restart_rect.collidepoint(mouse_x, mouse_y):
                    return "restart"
                elif back_to_menu_rect.collidepoint(mouse_x, mouse_y):
                    return "menu"
                

        # Draw the background
        screen.blit(pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/bg.jpg')), (0, 0))
        
        # Draw buttons
        draw_button_image(screen, resume_img, 60, 150)
        draw_button_image(screen, restart_img, 60, 220)
        draw_button_image(screen, back_img, 60, 290)
    
        pygame.display.flip()

def handle_settings_action(action):
    if action == "resume":
        print("Game Resumed")  # Thực hiện hành động khôi phục trò chơi
        return False  # Quay lại trò chơi
    elif action == "restart":
        print("Game Restarted")  # Thực hiện hành động khởi động lại trò chơi
        return True  # Quay lại trò chơi và khởi động lại
    elif action == "menu":
        print("Returning to Main Menu")  # Quay lại menu chính
        return "menu"  # Quay lại menu chính
