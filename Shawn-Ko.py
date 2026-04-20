import pygame

pygame.init()

#Screen
screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()

#colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
DARK_GRAY = (100, 100, 100)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

#Background Image
bck_img = pygame.image.load('SK-Assets/SK-background.png').convert()
bck_img = pygame.transform.scale(bck_img, (screen_width, screen_height))

#grid image
grid_img = pygame.image.load('SK-Assets/SK-grid.png').convert()
grid_img = pygame.transform.scale(grid_img, (screen_width//3, screen_height//2))
grid_img_rect = grid_img.get_rect()
grid_img_rect.bottomright = screen_rect.bottomright
grid_img_width = grid_img.get_width()
grid_img_height = grid_img.get_height()

#creating button for each alphabet
image_x = screen_width - grid_img_width
image_y = screen_height - grid_img_height
cell_width = grid_img_width // 3
cell_height = grid_img_height // 3
buttons = []
for row in range(3):
    for col in range(3):
        number = row * 3 + col + 1
        button_x = image_x + (col * cell_width)
        button_y = image_y + (row * cell_height)
        buttons.append([button_x, button_y, cell_width, cell_height, number, False])

#Level system
current_level = 1
total_levels = 5
level_complete = False
game_complete = False

# Password input system
password_input = ""
message = ""
message_timer = 0

#Enter button
enter_button_width = 120
enter_button_height = 50
enter_button_x = screen_width // 2 - enter_button_width // 2
enter_button_y = screen_height - 100
enter_button = [enter_button_x, enter_button_y, enter_button_width, enter_button_height, "ENTER", False]

# Placeholder for puzzles' logics
def check_puzzle_solution(level, password):
    if level == 1:
        return password == "123"
    elif level == 2:
        return password == "456"
    elif level == 3:
        return password == "789"
    elif level == 4:
        return password == "111"
    elif level == 5:
        return password == "999"
    return False


def load_level(level):
    global password_input, message, message_timer
    password_input = ""
    print(f"Loading Level {level}...")

    #Placeholder for puzzle setup
    #Puzzle initialization code will be put here
    if level == 1:
        pass
    elif level == 2:
        pass
    elif level == 3:
        pass
    elif level == 4:
        pass
    elif level == 5:
        pass


def complete_level():
    global current_level, level_complete, game_complete, message, message_timer, password_input

    if current_level < total_levels:
        current_level += 1
        level_complete = False
        password_input = ""
        message = f"Level {current_level - 1} Complete! Moving to Level {current_level}"
        message_timer = 90
        load_level(current_level)  # Load next level's puzzle
    else:
        game_complete = True
        message = "Congratulations! You completed all levels!"
        message_timer = 180


def reset_current_level():
    #Reset password when wrong
    global password_input, message, message_timer
    password_input = ""
    message = f"Wrong password! Level {current_level} reset. Try again!"
    message_timer = 90

    # ===== RESET PUZZLE FOR CURRENT LEVEL =====
    load_level(current_level)


# Load first level
load_level(1)

running = True
while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for button in buttons:
        x, y, width, height, number, hovered = button
        if (x < mouse_x < x + width) and (y < mouse_y < y + height):
            button[5] = True
        else:
            button[5] = False

    ex, ey, ew, eh, etext, ehovered = enter_button
    if (ex < mouse_x < ex + ew) and (ey < mouse_y < ey + eh):
        enter_button[5] = True
    else:
        enter_button[5] = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_complete and not level_complete:
            # Check grid button clicks
            for button in buttons:
                x, y, width, height, number, hovered = button
                if (x < mouse_x < x + width) and (y < mouse_y < y + height):
                    password_input += str(number)
                    if len(password_input) > 10:
                        password_input = password_input[:10]
                    print(f"Added {number} to password. Current: {password_input}")
                    break

            # Check ENTER button click
            if (ex < mouse_x < ex + ew) and (ey < mouse_y < ey + eh):
                print(f"ENTER pressed with password: {password_input}")
                if check_puzzle_solution(current_level, password_input):
                    level_complete = True
                    complete_level()
                else:
                    reset_current_level()

    screen.blit(bck_img, (0,0))
    screen.blit(grid_img, grid_img_rect)
    pygame.display.flip()
pygame.quit()