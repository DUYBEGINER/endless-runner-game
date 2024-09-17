import pygame
import sys, os
import Variables, menu

# Constants
WHITE = (255, 255, 255)

# Load button images
def load_button_images():
    resume_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/start.png'))
    restart_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/restart.png'))
    back_img = pygame.image.load(os.path.join(Variables.current_dir, 'Asset/Setting/back.png'))
    return resume_img, restart_img, back_img

def draw_button_image(screen, img, x, y):
    screen.blit(img, (x, y))

def settings_menu(screen, font):
    # Load button images
    resume_img, restart_img, back_to_menu_img = load_button_images()
    
    # Button positions
    start_rect = pygame.Rect(60, 150, resume_img.get_width(), resume_img.get_height())
    restart_rect = pygame.Rect(60, 220, restart_img.get_width(), restart_img.get_height())
    back_to_menu_rect = pygame.Rect(60, 290, back_to_menu_img.get_width(), back_to_menu_img.get_height())
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if start_rect.collidepoint(mouse_x, mouse_y):
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
        draw_button_image(screen, back_to_menu_img, 60, 290)
        
        pygame.display.flip()
