import pygame
import time
import os

pygame.init()

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "Main_menu", "Level_11", "Level_12")
def load_image(name):
    path = os.path.join(IMAGE_DIR, name)
    try:
        image = pygame.image.load(path).convert_alpha()
        return image
    except:
        print(f"File Not Found: {path}")
        return None

class picture:
    def __init__(self, image_name, x, y):
        self.name = load_image(image_name)
        self.x = x
        self.y = y


#==================================
# Main Menu
#==================================
brg = picture("menu_brg.jpg", 0,0)
display = pygame.display.set_mode((1200, 650), pygame.SCALED) 
display.blit(brg.name, (brg.x, brg.y))

exit_icon = pygame.image.load("exit_button.png")
exit_icon = pygame.transform.scale(exit_icon, (110, 75))
pygame.display.flip()


#==================================
# Set up the display screen
#==================================
pygame.display.set_caption("The Puzzle House")
icon = pygame.image.load("puzzle_icon.png")
pygame.display.set_icon(icon)


#==================================
# Button class
#==================================
class Button:
    def __init__(self, x, y):
        self.image = exit_icon
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, display):
        display.blit(self.image, self.rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)


exit_button = Button(1120, 580)
default_cursor = pygame.SYSTEM_CURSOR_ARROW
hand_cursor = pygame.SYSTEM_CURSOR_HAND


#==================================
# Game loop
#==================================
running = True
while running:
    exit_button.update(display)

    #cursor changing
    mouse_pos = pygame.mouse.get_pos()
    if exit_button.is_hovered(mouse_pos):
        pygame.mouse.set_cursor(hand_cursor)
    else:
        pygame.mouse.set_cursor(default_cursor)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.is_clicked(event.pos):
                running = False

    pygame.display.update()

pygame.quit()

# # Load images
# wall = pygame.image.load("wall.png")
# data = open("puzzle_00.png")
# puzzle = pygame.image.load(data, '.png')


# # Background and objects
# display.blit(wall, (0, 0))
# display.blit(puzzle, (100, 100))

# font = pygame.font.Font('C:\\Users\\HP\\OneDrive\\Documents\\PythonGame\\OpenSans-VariableFont_wdth,wght.ttf', 36)
# text = font.render("Hello, World!", True, (0,0,0))
# display.blit(text, (400, 300))

# # Update the display
# pygame.display.flip()

# time.sleep(2)
# text_1 = font.render("This is other screen", True, (0,0,0))
# display.blit(text_1, (0,0))
# wall2 = pygame.image.load("background.png")
# wall2 = pygame.transform.scale(wall2, (1000, 650))
# display.blit(wall2, (0, 0))
# pygame.display.flip()
# time.sleep(2)
