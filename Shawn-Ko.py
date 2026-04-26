import pygame

pygame.init()

#Screen
screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

#colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (202, 228, 241)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

#Background Image
bck_img = pygame.image.load('SK-Assets/SK-background.png').convert()
bck_img = pygame.transform.scale(bck_img, (screen_width, screen_height))


class Letter_Button:
    def __init__(self, x, y, image):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.letter = None
        self.visible = True
        self.clicked = False

    def draw(self):
        if self.visible:
            screen.blit(self.image, self.rect)

    def hide(self):
        self.visible = False
        self.clicked = True

# ========== Button Configuration ==========
# Right section dimensions
right_section_width = screen_width // 3
button_area_start_x = screen_width - right_section_width

# Picture loading
images = {}
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]

enter_img = pygame.image.load("assets/Button_alphabet/enter.png")
enter_img = pygame.transform.scale(enter_img, (45, 45))

for letter in letters:
    img = pygame.image.load(f"assets/Button_alphabet/letter_{letter}.png")
    images[letter] = pygame.transform.scale(img, (45, 45))

# Configure button grid
button_size = 45
button_gap = 80
buttons_per_row = 3
rows = 3

total_grid_width = buttons_per_row * button_gap
total_grid_height = rows * button_gap

# Letters grid start position (centered in the right section)
grid_start_x = button_area_start_x + (right_section_width - total_grid_width) // 2
grid_start_y = (screen_height - total_grid_height) // 2

# Create letter buttons
buttons = []
for i, letter in enumerate(letters):
    row = i // buttons_per_row
    col = i % buttons_per_row
    x = grid_start_x + col * button_gap
    y = grid_start_y + row * button_gap
    btn = Letter_Button(x, y, images[letter])
    btn.letter = letter
    buttons.append(btn)

# ENTER Button
enter_btn_x = grid_start_x + (total_grid_width // 2) - 22
enter_btn_y = grid_start_y + total_grid_height + 30
enter_btn = Letter_Button(enter_btn_x, enter_btn_y, enter_img)
enter_btn.letter = "ENTER"
buttons.append(enter_btn)

# Button Drawing
for btn in buttons:
    btn.draw()

#Level system
current_level = 1
total_levels = 5
level_complete = False
game_complete = False

# Password input system
password_input = []
message = ""
message_timer = 0

# Placeholder for puzzles' logics
def check_puzzle_solution(level, password):
    if level == 1:
        return password == ["a","b","c"]
    elif level == 2:
        return password == ["d","e","f"]
    elif level == 3:
        return password == ["g","h","i"]
    elif level == 4:
        return password == ['g','b','f']
    elif level == 5:
        return password == ['f','a','d']
    return False


def load_level(level):
    global password_input, message, message_timer
    password_input = []
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
        password_input = []
        message = f"Level {current_level - 1} Complete! Moving to Level {current_level}"
        message_timer = 90
        load_level(current_level)  # Load next level's puzzle
    else:
        game_complete = True
        message = "Congratulations! You completed all levels!"
        message_timer = 180


def reset_current_level():
    #Reset password when wrong
    global password_input, message, message_timer, buttons
    password_input = []
    message = f"Wrong password! Level {current_level} reset. Try again!"
    message_timer = 90
    for btn in buttons:
        if btn.letter != "ENTER":
            btn.visible = True
            btn.clicked = False

    # ===== RESET PUZZLE FOR CURRENT LEVEL =====
    load_level(current_level)


# Load first level
load_level(1)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_complete and not level_complete:
            # == Check LETTER button click ==
            if (clicked_btn := next((btn for btn in buttons if
                                     btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"),
                                    None)):
                if True:
                    password_input.append(clicked_btn.letter)
                    print(f"Clicked: {clicked_btn.letter}, passcode: {password_input}")
                    clicked_btn.hide()

            # == Check ENTER button click ==
            # Checking if the click is on the ENTER button and if it's visible (not hidden)
            elif (enter_clicked := next(
                    (btn for btn in buttons if btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"), None)):
                if True:
                    if check_puzzle_solution(current_level, password_input):
                        level_complete = True
                        complete_level()
                        print("✅ You passed!")

                    else:
                        reset_current_level()
                        # Reset buttons
                        print("Game reset. Try again.")

    screen.fill(LIGHT_BLUE)

    # Button drawing
    for btn in buttons:
        btn.draw()

    # Disappearing buttons
    for btn in buttons:
        if not btn.visible and btn.letter != "ENTER":
            font = pygame.font.Font(None, 36)
            check = font.render("", True, (0, 255, 0))
            screen.blit(check, (btn.rect.centerx - 15, btn.rect.centery - 15))

    # Draw Level Display
    level_text = font_large.render(f"Level {current_level}/{total_levels}", True, YELLOW)
    screen.blit(level_text, (20, 20))





    # Show message
    if message_timer > 0:
        msg_color = GREEN if "Complete" in message or "Congratulations" in message else RED
        msg_surface = font_medium.render(message, True, msg_color)
        msg_x = (screen_width - msg_surface.get_width()) // 2
        msg_y = screen_width - 60
        screen.blit(msg_surface, (msg_x, msg_y))
        message_timer -= 1

    # Show game complete overlay
    if game_complete:
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(200)
        overlay.fill(WHITE)
        screen.blit(overlay, (0, 0))

        complete_text1 = font_large.render("GAME COMPLETE!", True, GREEN)
        complete_text2 = font_medium.render("You've completed all levels!", True, BLUE)
        complete_text3 = font_small.render("Close the window to quit", True, BLACK)

        screen.blit(complete_text1, (screen_width // 2 - complete_text1.get_width() // 2, screen_height // 2 - 50))
        screen.blit(complete_text2, (screen_width // 2 - complete_text2.get_width() // 2, screen_height // 2))
        screen.blit(complete_text3, (screen_width // 2 - complete_text3.get_width() // 2, screen_height // 2 + 50))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()