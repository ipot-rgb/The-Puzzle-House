import pygame
import time
import os 
from instruction import show_instruction
from hints_system import HintManager

# Import level modules
import importlib
levels = {}

for i in range(9):
    module = importlib.import_module(f"level_{i}")

    levels[i] = (
        f"level_{i}",
        getattr(module, f"run_level_{i}")
    )

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

setting_icon = pygame.image.load(os.path.join(ASSETS_DIR, "Icon", "setting_button.png"))
setting_icon = pygame.transform.scale(setting_icon, (55, 55))
setting_button = Button(45, 45, setting_icon)
setting_button.update(display)



pygame.display.flip()

hint_manager = HintManager()

#Level system
current_level = 0
total_levels = 9
level_complete = False
game_complete = False

#password input system

message = ""
message_timer = 0

# ===============================
# Level transition function
# ===============================

def show_level_complete_transition(screen, completion_time):
    clock = pygame.time.Clock()
    black_surf = pygame.Surface(screen.get_size())
    black_surf.fill((0, 0, 0))

    #Fonts
    font_big = pygame.font.Font('Notable-Regular.ttf', 70)
    font_small = pygame.font.Font('Notable-Regular.ttf', 40)

    #Texts
    congrats_text = font_big.render("Congratulations!", True, (0, 128, 0))
    time_text = font_small.render(f"Level finished in {completion_time:.2f} s", True, (200, 200, 200))

    #Positions
    congrats_rect = congrats_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    time_rect = time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    #Fade in "Congratulations!"
    for alpha in range(0, 256, 5):
        screen.blit(black_surf, (0, 0))
        congrats_text.set_alpha(alpha)
        screen.blit(congrats_text, congrats_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.time.wait(1000)

    #Fade in time text
    for alpha in range(0, 256, 5):
        screen.blit(black_surf, (0, 0))
        congrats_text.set_alpha(255)
        screen.blit(congrats_text, congrats_rect)
        time_text.set_alpha(alpha)
        screen.blit(time_text, time_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.time.wait(2000)

# ===============================
# LEVEL FUNCTION MAP
# ===============================
def load_level(level):
    global message, message_timer, current_screen
    print(f"Loading Level {level}...")

    if level in levels:
        current_screen = levels[level][0]   # "level_x"
    else:
        current_screen = "menu"

    return current_screen

def complete_level(completion_time):
    global current_level, level_complete, game_complete
    global message, message_timer, current_screen

    if completion_time is not None:
        show_level_complete_transition(display, completion_time)
    else :
        pygame.time.wait(1000)

    if current_level < total_levels:
        message = f"Level {current_level} Complete! Moving to Level {current_level + 1}"
        message_timer = 90

        current_level += 1
        level_complete = False

        load_level(current_level)

        print(f"Moving to level {current_level}")

    else:
        game_complete = True
        message = "Congratulations! You completed all levels!"
        message_timer = 180
        current_screen = "menu"

        print("Game complete!")
        time.sleep(2)

#===============================
# Game loop
#===============================
settings_open = False
running = True
current_screen = "menu"
menu_list = [1,2,3,4,5,6,7,8,9,0]
while running:
    mouse_pos = pygame.mouse.get_pos()

    # ===============================
    # MENU
    # ===============================
    if current_screen == "menu":
        display.blit(brg.name, (brg.x, brg.y))

        text_title = font.render("The Puzzle House", True, (0, 0, 0))
        display.blit(text_title, (250, 100))

        exit_button.update(display)
        start_button.update(display)
        setting_button.update(display)

        if exit_button.is_hovered(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)
        elif start_button.is_hovered(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)
        elif setting_button.is_hovered(mouse_pos):
            pygame.mouse.set_cursor(hand_cursor)
        else:
            pygame.mouse.set_cursor(default_cursor)

        # Settings overlay
        if settings_open:
            overlay = pygame.Surface(display.get_size())
            overlay.fill((0,0,0))
            overlay.set_alpha(150)

            display.blit(overlay, (0,0))
            menu_rect = pygame.Rect(350,150,500,300)

            pygame.draw.rect(display,(40,40,40),menu_rect)
            pygame.draw.rect(display,(255,255,255),menu_rect,3)

            settings_text = font.render("SETTINGS",True,(255,255,255))
            display.blit(settings_text,(420,180))

    # ===============================
    # LEVEL HANDLER
    # ===============================
    elif current_screen.startswith("level_"):

        # level function
        for lvl, (name, func) in levels.items():
            if name == current_screen:
                result = func(display, hint_manager)   # can be str or tuple
                break
        else:
            result = None

        # ===============================
        # RESULT HANDLING
        # ===============================
        if isinstance(result, tuple) and result[0] == "complete":
            completion_time = result[1]
            complete_level(completion_time)
        elif result == "menu":
            current_screen = "menu"
        elif result == "quit":
            running = False
        elif result == "complete":  # fallback for old levels without timer
            complete_level(None)


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ~~~~~ Handle button clicks ~~~~~
        if event.type == pygame.MOUSEBUTTONDOWN:
            if exit_button.is_clicked(event.pos):
                exit_se = pygame.mixer.Sound("assets/sound_effect/exit_se.wav")
                exit_se.play()
                pygame.time.delay(1750)
                running = False
            if start_button.is_clicked(event.pos):
                whoop = pygame.mixer.Sound("assets/sound_effect/whoop_se.wav")
                whoop.play()
                instruction_font = pygame.font.Font('Notable-Regular.ttf', 28)
                show_instruction(display, instruction_font)
                load_level(current_level)
            if setting_button.is_clicked(event.pos):
                settings_open = not settings_open
                pygame.display.update()

    pygame.display.update()
pygame.quit()