import pygame
import sys
import importlib  # For dynamic loading of level modules

# ===== INITIALIZATION =====
pygame.init()

# Screen
screen_width = 1200
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()

# Colors
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


# ===== BUTTON CLASS =====
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


# ===== BUTTON CONFIGURATION =====
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

# ===== LEVEL SYSTEM =====
current_level = 1
total_levels = 5
level_complete = False
game_complete = False

# Password input system
password_input = []
message = ""
message_timer = 0


# ===== LEVEL GAME INTEGRATION =====
class LevelManager:
    """Manages loading and running level games"""

    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_level_game = None

    def load_level(self, level_number):
        """Dynamically load and return a level game module"""
        try:
            # Method 1: Each level is a separate Python file
            module_name = f"levels.level_{level_number}"
            level_module = importlib.import_module(module_name)

            # Create the level game instance
            level_game_class = getattr(level_module, "LevelGame")
            return level_game_class(self.screen, self.screen_width, self.screen_height)

        except ImportError:
            # Method 2: If file doesn't exist, use placeholder
            print(f"Level {level_number} not found, using placeholder")
            return PlaceholderLevel(level_number, self.screen, self.screen_width, self.screen_height)

    def run_level(self, level_number):
        """Run a level and return result (True if beaten, False if quit)"""
        level_game = self.load_level(level_number)
        return level_game.run()


class PlaceholderLevel:
    """Fallback level when actual level file doesn't exist"""

    def __init__(self, level_num, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_num = level_num
        self.running = True
        self.level_complete = False
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.level_complete = True
        return True

    def update(self):
        pass

    def draw(self):
        self.screen.fill((50, 50, 100))
        font = pygame.font.Font(None, 74)
        text1 = font.render(f"Level {self.level_num} Placeholder", True, WHITE)
        text2 = pygame.font.Font(None, 36).render("Press SPACE to complete level", True, YELLOW)

        self.screen.blit(text1, (self.screen_width // 2 - text1.get_width() // 2,
                                 self.screen_height // 2 - 50))
        self.screen.blit(text2, (self.screen_width // 2 - text2.get_width() // 2,
                                 self.screen_height // 2 + 50))

    def run(self):
        while self.running:
            if not self.handle_events():
                return False
            self.update()
            self.draw()

            if self.level_complete:
                return True

            pygame.display.flip()
            self.clock.tick(60)
        return False


# ===== PUZZLE LOGIC =====
def check_puzzle_solution(level, password):
    if level == 1:
        return password == ["a", "b", "c"]
    elif level == 2:
        return password == ["d", "e", "f"]
    elif level == 3:
        return password == ["g", "h", "i"]
    elif level == 4:
        return password == ['g', 'b', 'f']
    elif level == 5:
        return password == ['f', 'a', 'd']
    return False


def load_level(level):
    """Reset the password system for a new level"""
    global password_input, message, message_timer
    password_input = []
    print(f"Level {level} password system ready")

    # Reset all letter buttons
    for btn in buttons:
        if btn.letter != "ENTER":
            btn.visible = True
            btn.clicked = False


def complete_level():
    global current_level, level_complete, game_complete, message, message_timer, password_input

    if current_level < total_levels:
        current_level += 1
        level_complete = False
        password_input = []
        message = f"Level {current_level - 1} Complete! Moving to Level {current_level}"
        message_timer = 90
        load_level(current_level)
    else:
        game_complete = True
        message = "Congratulations! You completed all levels!"
        message_timer = 180


def reset_current_level():
    global password_input, message, message_timer, buttons
    password_input = []
    message = f"Wrong password! Level {current_level} reset. Try again!"
    message_timer = 90
    for btn in buttons:
        if btn.letter != "ENTER":
            btn.visible = True
            btn.clicked = False
    load_level(current_level)


# ===== MAIN MENU SYSTEM =====
class MainMenu:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.options = ["Start Game", "Instructions", "Quit"]
        self.selected = 0
        self.clock = pygame.time.Clock()

    def draw(self):
        self.screen.fill(LIGHT_BLUE)

        # Title
        title_font = pygame.font.Font(None, 84)
        title = title_font.render("PUZZLE ADVENTURE", True, BLUE)
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 100))

        # Menu options
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else BLACK
            option_font = pygame.font.Font(None, 48)
            text = option_font.render(option, True, color)
            y_pos = 300 + i * 80
            self.screen.blit(text, (self.screen_width // 2 - text.get_width() // 2, y_pos))

        pygame.display.flip()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected] == "Start Game":
                            return "start"
                        elif self.options[self.selected] == "Instructions":
                            return "instructions"
                        elif self.options[self.selected] == "Quit":
                            return "quit"

            self.draw()
            self.clock.tick(60)


class InstructionsScreen:
    def run(self, screen, screen_width, screen_height):
        waiting = True
        clock = pygame.time.Clock()

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        waiting = False

            screen.fill(LIGHT_BLUE)

            # Instructions text
            font = pygame.font.Font(None, 36)
            instructions = [
                "HOW TO PLAY:",
                "",
                "1. Click letter buttons to enter password",
                "2. Press ENTER to submit",
                "3. Complete the puzzle to advance levels",
                "",
                "Press SPACE or ESC to return to menu"
            ]

            for i, line in enumerate(instructions):
                color = BLUE if i == 0 else BLACK
                text = font.render(line, True, color)
                screen.blit(text, (100, 100 + i * 40))

            pygame.display.flip()
            clock.tick(60)

        return "menu"


# ===== MAIN GAME LOADER =====
def run_level_with_password(level_number):
    """Run the password system for a level, then launch actual game"""
    global current_level, level_complete, game_complete

    # Reset state for this level
    level_complete = False
    load_level(level_number)

    # Password input loop
    waiting_for_password = True
    clock = pygame.time.Clock()

    while waiting_for_password:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.MOUSEBUTTONDOWN and not game_complete and not level_complete:
                # Check letter button clicks
                clicked_btn = next((btn for btn in buttons if
                                    btn.rect.collidepoint(event.pos) and btn.visible and btn.letter != "ENTER"), None)
                if clicked_btn:
                    password_input.append(clicked_btn.letter)
                    print(f"Clicked: {clicked_btn.letter}, passcode: {password_input}")
                    clicked_btn.hide()

                # Check enter button
                enter_clicked = next((btn for btn in buttons if
                                      btn.rect.collidepoint(event.pos) and btn.letter == "ENTER"), None)
                if enter_clicked:
                    if check_puzzle_solution(level_number, password_input):
                        level_complete = True
                        waiting_for_password = False  # Exit password screen
                        return "start_game"
                    else:
                        reset_current_level()
                        print("Wrong password! Try again.")

        # Draw password screen
        screen.fill(LIGHT_BLUE)

        # Draw buttons
        for btn in buttons:
            btn.draw()

        # Draw level display
        level_text = font_large.render(f"Level {level_number}/{total_levels}", True, YELLOW)
        screen.blit(level_text, (20, 20))

        # Draw password display
        password_display = "Password: " + " ".join(password_input).upper()
        pass_text = font_medium.render(password_display, True, BLUE)
        screen.blit(pass_text, (20, 80))

        # Draw message
        if message_timer > 0:
            msg_color = GREEN if "Complete" in message or "Congratulations" in message else RED
            msg_surface = font_medium.render(message, True, msg_color)
            msg_x = (screen_width - msg_surface.get_width()) // 2
            msg_y = screen_height - 60
            screen.blit(msg_surface, (msg_x, msg_y))
            message_timer -= 1

        pygame.display.flip()
        clock.tick(60)

    return "start_game"


# ===== MAIN FUNCTION =====
def main():
    global current_level

    # Create level manager
    level_manager = LevelManager(screen, screen_width, screen_height)

    # Main game state
    game_state = "menu"  # menu, playing, instructions, quit

    while game_state != "quit":
        if game_state == "menu":
            menu = MainMenu(screen, screen_width, screen_height)
            result = menu.run()
            if result == "start":
                game_state = "playing"
                current_level = 1  # Reset to level 1
            elif result == "instructions":
                game_state = "instructions"
            elif result == "quit":
                game_state = "quit"

        elif game_state == "instructions":
            instructions = InstructionsScreen()
            result = instructions.run(screen, screen_width, screen_height)
            game_state = "menu" if result == "menu" else "quit"

        elif game_state == "playing":
            # Loop through all levels
            while current_level <= total_levels:
                # First, password screen
                password_result = run_level_with_password(current_level)

                if password_result == "quit":
                    game_state = "quit"
                    break

                # Then, run the actual game level
                if password_result == "start_game":
                    print(f"Starting Level {current_level} game...")
                    level_beaten = level_manager.run_level(current_level)

                    if level_beaten:
                        # Move to next level
                        if current_level < total_levels:
                            current_level += 1
                            message = f"Great! Moving to Level {current_level}"
                            message_timer = 90
                        else:
                            # Game complete!
                            game_state = "menu"
                            show_game_complete()
                            break
                    else:
                        # Player quit during level
                        game_state = "quit"
                        break

            if current_level > total_levels:
                game_state = "menu"


def show_game_complete():
    """Show game complete screen"""
    waiting = True
    clock = pygame.time.Clock()

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

        screen.fill(LIGHT_BLUE)
        complete_text1 = font_large.render("GAME COMPLETE!", True, GREEN)
        complete_text2 = font_medium.render("You've completed all levels!", True, BLUE)
        complete_text3 = font_small.render("Press any key to return to menu", True, BLACK)

        screen.blit(complete_text1, (screen_width // 2 - complete_text1.get_width() // 2, screen_height // 2 - 50))
        screen.blit(complete_text2, (screen_width // 2 - complete_text2.get_width() // 2, screen_height // 2))
        screen.blit(complete_text3, (screen_width // 2 - complete_text3.get_width() // 2, screen_height // 2 + 50))

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()