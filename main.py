import pygame
import time
import os 
from level_1 import run_level_1
from level_7 import run_level_7
from level_8 import run_level_8

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
font = pygame.font.Font('Notable-Regular.ttf', 60)

# Update the display
pygame.display.flip()

# Cursors
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

#Level system
current_level = 1
total_levels = 9
level_complete = False
game_complete = False

# Password input system

message = ""
message_timer = 0


def load_level(level):
    global message, message_timer, current_screen
    print(f"Loading Level {level}...")

    # Fixed logic - this will work correctly
    if level == 1:
        current_screen = "level_1"
    elif level == 2:
        current_screen = "level_7"  # You'll need to create level_2
    elif level == 3:
        current_screen = "level_8"  # Create level_3
    elif level == 4:
        current_screen = "level_4"  # Create level_4
    elif level == 5:
        current_screen = "level_5"  # Create level_5
    elif level == 6:
        current_screen = "level_6"  # Create level_6
    elif level == 7:
        current_screen = "level_2"

    elif level == 8:
        current_screen = "level_8"  # Create level_8
    elif level == 9:
        current_screen = "level_9"  # Create level_9
    else:
        current_screen = "menu"

    return current_screen


def complete_level():
    global current_level, level_complete, game_complete, message, message_timer, current_screen

    if current_level < total_levels:
        current_level += 1
        level_complete = False
        message = f"Level {current_level - 1} Complete! Moving to Level {current_level}"
        message_timer = 90
        load_level(current_level)  # Load next level's puzzle
        print(f"Moving to level {current_level}")
    else:
        game_complete = True
        message = "Congratulations! You completed all levels!"
        message_timer = 180
        current_screen = "menu"
        print("Game complete!")
        time.sleep(2)

def Game_Status(gamestatus) :
    if gamestatus :
        complete_level()

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
        text_title = font.render("The Puzzle House", True, (0, 0, 0))
        display.blit(text_title, (250, 100))
        exit_button.update(display)
        start_button.update(display)
        if exit_button.is_hovered(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)
        elif start_button.is_hovered(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)
        else:
            pygame.mouse.set_cursor(default_cursor)
            
    # REMEMBER CHANGE IT TO READABLE LEVEL NAMES LATER
    elif current_screen == "level_1":
        result = run_level_1(display)
        if result == "menu":
            current_screen = "menu"
        elif result == "quit":
            running = False
        elif result == "complete":  # Add this
            complete_level()

    elif current_screen == "level_7":
        result = run_level_7(display)
        if result == "menu":
            current_screen = "menu"
        elif result == "quit":
            running = False
        elif result == "complete":  # Add this
            complete_level()

    elif current_screen == "level_8":
        result = run_level_8(display)
        if result == "menu":
            current_screen = "menu"
        elif result == "quit":
            running = False
        elif result == "complete":  # Add this
            complete_level()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ~~~~~ Handle button clicks ~~~~~
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.is_clicked(event.pos):
                running = False
                
            if start_button.is_clicked(event.pos):
                load_level(current_level)


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