import pygame
import time
import os 

#===============================
# Button class
#===============================
class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, display):
        display.blit(self.image, self.rect)
    
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

#===============================
# Picture class
#===============================

class picture:
    def __init__(self, path_parts, x, y):
        path = os.path.join(ASSETS_DIR, *path_parts)
        self.name = pygame.image.load(path)
        self.x = x
        self.y = y

pygame.init()

BASE_DIR = os.path.dirname(__file__)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


#===============================
# Set up the display screen
#===============================
display = pygame.display.set_mode((1200, 650), pygame.SCALED) 
pygame.display.set_caption("The Puzzle House")
icon = pygame.image.load(os.path.join(ASSETS_DIR, "Icon","puzzle_icon.png"))
pygame.display.set_icon(icon)

brg = picture(("Menu_interface", "menu_brg.jpg"), 0, 0)
display.blit(brg.name, (brg.x, brg.y))

default_cursor = pygame.SYSTEM_CURSOR_ARROW
hand_cursor = pygame.SYSTEM_CURSOR_HAND

#===============================
# Main Menu
#===============================

exit_icon = pygame.image.load(os.path.join(ASSETS_DIR, "Icon", "exit_button.png"))
exit_icon = pygame.transform.scale(exit_icon, (110, 75))
exit_button = Button(1125, 587, exit_icon)
exit_button.update(display)

start_icon = pygame.image.load(os.path.join(ASSETS_DIR, "Icon", "start_button.png"))
start_icon = pygame.transform.scale(start_icon, (175, 75))
start_button = Button(600, 265, start_icon)
start_button.update(display)
pygame.display.flip()


# --Game Class--
def tuto():
    pygame.mouse.set_cursor(default_cursor)
    pygame.display.set_caption("The Puzzle House - Tutorial")
    display.fill((255, 255, 255))
    font = pygame.font.Font('C:\\Users\\HP\\OneDrive\\Documents\\PythonGame\\GideonRoman-Regular.ttf', 36)
    text = font.render("Tutorial", True, (0,0,0))
    display.blit(text, (400, 300))
    pygame.display.flip()

def level_1():
    pygame.mouse.set_cursor(default_cursor)
    while True:
        pass

def level_2():
    pygame.mouse.set_cursor(default_cursor)
    while True:
        pass

def level_3():
    pygame.mouse.set_cursor(default_cursor)
    while True:
        pass

def level_4():
    pygame.mouse.set_cursor(default_cursor)
    while True:
        pass

def level_5():
    pygame.mouse.set_cursor(default_cursor)
    while True:
        pass


#===============================
# Game loop
#===============================
running = True
current_screen = "menu"
while running:
    mouse_pos = pygame.mouse.get_pos()

    # ~~ Display Main Menu
    if current_screen == "menu":
        display.blit(brg.name, (brg.x, brg.y))
        exit_button.update(display)
        start_button.update(display)
        if exit_button.is_hovered(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)
        elif start_button.is_hovered(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)
        else:
            pygame.mouse.set_cursor(default_cursor)

    # ~~ Display Game Screen
    elif current_screen == "game":
        tuto()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ~~~~~ Handle button clicks ~~~~~
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.is_clicked(event.pos):
                running = False
            if start_button.is_clicked(event.pos):
                current_screen = "game"
                
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
