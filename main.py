import pygame
import time
import os 
import settings
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

pygame.mixer.init()
pygame.mixer.music.load(os.path.join("materials", "bgm", "menu_bgm.mp3"))
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1)

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

on_icon = pygame.image.load("assets/Icon/on_button.png")
on_icon = pygame.transform.scale(on_icon, (75, 55))
on_button = Button(700, 315, on_icon)

off_icon = pygame.image.load("assets/Icon/off_button.png")  
off_icon = pygame.transform.scale(off_icon, (75, 55))
off_button = Button(700, 315, off_icon)

close_icon = pygame.image.load(os.path.join(ASSETS_DIR, "Icon", "close_icon.png"))
close_icon = pygame.transform.scale(close_icon, (23, 23))
close_button = Button(820, 170, close_icon)

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

# Global settings state
settings_open = False

def cleanup_level():
    import gc
    global settings_open
    
    # Reset settings state
    settings_open = False

    for surface in gc.get_objects():
        if isinstance(surface, pygame.Surface):
            pass

    gc.collect()

# ===============================
# Level transition function
# ===============================
def level_transition(screen, completion_time):
    pygame.mixer.music.stop()

    clock = pygame.time.Clock()
    black_surf = pygame.Surface(screen.get_size())
    black_surf.fill((0, 0, 0))

    #fonts
    font_big = pygame.font.Font('Notable-Regular.ttf', 70)
    font_small = pygame.font.Font('Notable-Regular.ttf', 40)

    #texts
    congrats_text = font_big.render("Congratulations!", True, (0, 128, 0))
    time_text = font_small.render(f"Level finished in {completion_time:.2f} s", True, (200, 200, 200))

    #positions
    congrats_rect = congrats_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
    time_rect = time_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))

    #fade in "Congratulations!"
    for alpha in range(0, 256, 5):
        screen.blit(black_surf, (0, 0))
        congrats_text.set_alpha(alpha)
        screen.blit(congrats_text, congrats_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.time.wait(1000)

    #fade in timer text
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
# Transition page for level 0
# ===============================
def tutorial_transition(screen):
    #stop music and put on sound effect
    pygame.mixer.music.stop()
    sound_tutorial = pygame.mixer.Sound("assets/sound_effect/tutorial_se.wav")
    sound_tutorial.play()
    time.sleep(1)

    clock = pygame.time.Clock()
    black_surf = pygame.Surface(screen.get_size())
    black_surf.fill((0, 0, 0))

    #fonts
    font_big = pygame.font.Font('Notable-Regular.ttf', 70)
    font_small = pygame.font.Font('Notable-Regular.ttf', 40)

    #screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    #part 1: "Congratulations!"
    congrats_text = font_big.render("Congratulations!", True, (0, 128, 0))
    congrats_rect = congrats_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

    for alpha in range(0, 256, 5):
        screen.blit(black_surf, (0, 0))
        congrats_text.set_alpha(alpha)
        screen.blit(congrats_text, congrats_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.time.wait(1000)

    for alpha in range(0, 256, 5):
        screen.blit(black_surf, (0, 0))
        congrats_text.set_alpha(255)
        screen.blit(congrats_text, congrats_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.time.wait(1000)

    #part 2: transition to show "Welcome To The Puzzle House"
    for alpha in range(255, -1, -5):
        screen.blit(black_surf, (0, 0))
        congrats_text.set_alpha(alpha)
        screen.blit(congrats_text, congrats_rect)
        pygame.display.flip()
        clock.tick(60)

    welcome_text = font_small.render("Welcome", True, (200, 200, 200))
    welcome_rect = welcome_text.get_rect(center=(screen_width // 2 - 100, screen_height // 2 - 50))

    for alpha in range(0, 256, 5):
        screen.blit(black_surf, (0, 0))
        welcome_text.set_alpha(alpha)
        screen.blit(welcome_text, welcome_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.time.wait(450)

    to_text = font_small.render("To", True, (200, 200, 200))
    to_rect = to_text.get_rect(midleft=(welcome_rect.right + 20, welcome_rect.centery))

    for alpha in range(0, 256, 5):
        screen.blit(black_surf, (0, 0))
        welcome_text.set_alpha(255)
        screen.blit(welcome_text, welcome_rect)
        to_text.set_alpha(alpha)
        screen.blit(to_text, to_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.time.wait(450)

    title_text = font_big.render("The Puzzle House", True, (0,128,0))
    title_rect = title_text.get_rect(center=(screen_width // 2, welcome_rect.bottom + 60))

    for alpha in range(0, 256, 5):
        screen.blit(black_surf, (0, 0))
        welcome_text.set_alpha(255)
        screen.blit(welcome_text, welcome_rect)
        to_text.set_alpha(255)
        screen.blit(to_text, to_rect)
        title_text.set_alpha(alpha)
        screen.blit(title_text, title_rect)
        pygame.display.flip()
        clock.tick(60)

    start_time = time.time()
    while time.time() - start_time < 2:
        screen.blit(black_surf, (0, 0))
        welcome_text.set_alpha(255)
        screen.blit(welcome_text, welcome_rect)
        to_text.set_alpha(255)
        screen.blit(to_text, to_rect)
        title_text.set_alpha(255)
        screen.blit(title_text, title_rect)
        pygame.display.flip()
        clock.tick(60)

    for alpha in range(255, -1, -5):
        screen.blit(black_surf, (0, 0))
        welcome_text.set_alpha(alpha)
        screen.blit(welcome_text, welcome_rect)
        to_text.set_alpha(alpha)
        screen.blit(to_text, to_rect)
        title_text.set_alpha(alpha)
        screen.blit(title_text, title_rect)
        pygame.display.flip()
        clock.tick(60)

    pygame.time.wait(500)

preserved_states = {}

# ===============================
# LEVEL FUNCTION MAP
# ===============================
def load_level(level):
    global message, message_timer, current_screen, settings_open
    
    # Reset settings state when loading a level
    settings_open = False
    
    print(f"Loading Level {level}...")

    pygame.mixer.music.stop()

    if level in levels:
        current_screen = levels[level][0]   # "level_x"
    else:
        current_screen = "menu"

    return current_screen

def complete_level(completion_time):
    global current_level, level_complete, game_complete
    global message, message_timer, current_screen, settings_open

    # Reset settings state when completing a level
    settings_open = False

    if completion_time is not None:
        level_transition(display, completion_time)
    else:
        pygame.time.wait(1000)

    if current_level == 0:
        tutorial_transition(display)

    cleanup_level()

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

            if settings.music_on:
                on_button.update(display)
            else:
                off_button.update(display)

            music_text = pygame.font.Font('Notable-Regular.ttf', 25)
            text = music_text.render("Music", True, (255,255,255))
            display.blit(text, (450,300))

            close_button.update(display)

    # ===============================
    # LEVEL HANDLER
    # ===============================
    elif current_screen.startswith("level_"):
        preserve_state = preserved_states.get(current_screen, False)

        # level function
        for lvl, (name, func) in levels.items():
            if name == current_screen:
                result = func(display, hint_manager, preserve_state=preserve_state)
                break
        else:
            result = None

        # ===============================
        # RESULT HANDLING
        # ===============================
        if isinstance(result, tuple):
            if result[0] == "complete":
                completion_time = result[1]
                complete_level(completion_time)
                preserved_states[current_screen] = False
            elif result[0] == "refresh":
                preserved_states[current_screen] = True
                continue

        elif result == "menu":
            current_screen = "menu"
            settings_open = False
        elif result == "quit":
            running = False
        elif result == "complete":  #fallback for old levels without timer
            complete_level(None)

    # ===============================
    # EVENT HANDLING
    # ===============================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ~~~~~ Handle button clicks ~~~~~
        if event.type == pygame.MOUSEBUTTONDOWN:
            if setting_button.is_clicked(event.pos):
                settings_se = pygame.mixer.Sound("assets/sound_effect/setting_se.wav")
                settings_se.play()
                settings_open = not settings_open

            elif settings_open:    
                if close_button.is_clicked(event.pos):
                    settings_open = False

                elif settings.music_on and on_button.is_clicked(event.pos):
                    settings.music_on = False
                    pygame.mixer.music.set_volume(0)
                    print("music is off")

                elif (not settings.music_on) and off_button.is_clicked(event.pos):
                    settings.music_on = True
                    pygame.mixer.music.set_volume(0.25)
                    print('music is on')
                    
                if close_button.is_hovered(mouse_pos):
                    pygame.mouse.set_cursor(hand_cursor)

                elif settings.music_on and on_button.is_hovered(mouse_pos):
                    pygame.mouse.set_cursor(hand_cursor)

                elif (not settings.music_on) and off_button.is_hovered(mouse_pos):
                    pygame.mouse.set_cursor(hand_cursor)

                else:
                    pygame.mouse.set_cursor(default_cursor)
                    
            else:
                if exit_button.is_clicked(event.pos):
                    exit_se = pygame.mixer.Sound("assets/sound_effect/exit_se.wav")
                    exit_se.play()
                    pygame.time.delay(1750)
                    running = False

                elif start_button.is_clicked(event.pos):
                    whoop = pygame.mixer.Sound("assets/sound_effect/whoop_se.wav")
                    whoop.play()
                    pygame.mixer.music.stop()
                    instruction_font = pygame.font.Font('Notable-Regular.ttf', 28)
                    show_instruction(display, instruction_font)
                    load_level(current_level)

    pygame.display.update()

pygame.quit()